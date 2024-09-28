import enum
import threading
import time
import uuid

from kubernetes import client, config
from kubernetes.client import ApiException
from kubernetes.stream import stream
from websocket import WebSocketBadStatusException

from olimar.job.job_command import JobStep
from olimar.job.job_config import JobConfig
from olimar.job.job_result import JobResult
from olimar.node.node import Node
from olimar.util.logger import Logger
from olimar.util.waitable import Waitable


# Load the kubeconfig file
config.load_kube_config()


class JobWaitable(Waitable):
    pass


class Job:
    NAMESPACE = 'default'
    BATCH_API = client.BatchV1Api()
    CORE_API = client.CoreV1Api()

    class Status(enum.Enum):
        NOT_STARTED = "Not Started"
        EXECUTING = "Executing"
        PENDING = "Pending"
        IDLE = "Idle"
        COMPLETE = "Completed"
        ERROR = "Error"

    def __init__(self, name, waitable, job_config: JobConfig, image, node: Node):
        self.name = name
        self.waitable = waitable
        self.config = job_config
        self.image = image
        self.node = node
        self.step_index = 0
        self.status = Job.Status.NOT_STARTED
        self.logger = Logger.get()
        self.thread = None

    @property
    def current_step(self) -> JobStep:
        return self.config.steps[self.step_index]

    def start(self):
        self.logger.info(f"Starting new pod: {self.name}")

        container = client.V1Container(
            name="my-container",
            image=self.image.to_link(),
            command=['sleep', 'infinity'],
            args=[],
            volume_mounts=[
                client.V1VolumeMount(
                    name="my-volume",
                    mount_path="/artifacts"
                ),
                client.V1VolumeMount(
                    name="dev-volume",  # Mount the /dev directory to access USB devices
                    mount_path="/dev"
                ),
            ],
            security_context=client.V1SecurityContext(
                privileged=True  # Provide privileged access to the container
            ),
        )

        host_artifact_mount = '/mnt/artifacts'
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"pod-name": self.name}),
            spec=client.V1PodSpec(
                containers=[container],
                restart_policy="Never",
                node_selector={"kubernetes.io/hostname": self.node.name},  # This assigns the pod to a specific node
                volumes=[
                    client.V1Volume(
                        name="my-volume",
                        host_path=client.V1HostPathVolumeSource(
                            path=host_artifact_mount,
                            type='DirectoryOrCreate'
                        ),
                    ),
                    client.V1Volume(
                        name="dev-volume",
                        host_path=client.V1HostPathVolumeSource(
                            path="/dev",  # Mount the host's /dev directory
                            type=None  # Optional: specify 'Directory' or other types as needed
                        )
                    )
                ],
            )
        )

        # Define the pod
        kubernetes_pod = client.V1Pod(
            api_version="v1",
            kind="Pod",
            metadata=client.V1ObjectMeta(name=self.name),
            spec=template.spec  # Use the spec from the template directly
        )

        # Create the pod
        self.CORE_API.create_namespaced_pod(
            namespace=self.NAMESPACE,
            body=kubernetes_pod
        )
        self.status = Job.Status.PENDING
        self.logger.info(f"Pod {self.name} created")

    def check_pending(self) -> None:
        pod = self.CORE_API.read_namespaced_pod(self.name, self.NAMESPACE)
        self.logger.info(f"{self.name} is {pod.status.phase}")
        if pod.status.phase == 'Running' and all(
                container.ready for container in pod.status.container_statuses):
            self.status = self.Status.IDLE

    def get_next_step(self) -> [JobStep, None]:
        try:
            step = self.config.steps[self.step_index]
            self.step_index += 1
        except IndexError:
            return None
        else:
            return step

    def start_step(self, step: JobStep):
        try:
            command = ['sh', '-c', step.command]
            self.logger.info(f"Executing on {self.node.name}: {command}")

            # Stream the command output in real-time
            resp = stream(
                self.CORE_API.connect_get_namespaced_pod_exec,
                self.name,
                self.NAMESPACE,
                container='my-container',
                command=command,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False,
                _preload_content=False  # Disable preloading to stream the output
            )
        except Exception as e:
            self.logger.error(f"Error executing command: {str(e)}")
            self.status = Job.Status.ERROR
            return

        def listener():
            nonlocal resp
            while resp.is_open():
                resp.update(timeout=1)
                if resp.peek_stdout():
                    output_chunk = resp.read_stdout()
                    step.response += output_chunk
                if resp.peek_stderr():
                    error_chunk = resp.read_stderr()
                    step.response += error_chunk
                time.sleep(0.5)

            resp.close()
            step.is_complete = True
            self.status = Job.Status.IDLE

        # Set status to EXECUTING and start the command execution in a separate thread
        self.status = Job.Status.EXECUTING
        thread = threading.Thread(target=listener)
        thread.start()

    def cleanup(self):
        self.status = Job.Status.COMPLETE
        # self.delete()
        job_result = JobResult(self.name, self.config.steps, [])
        self.waitable.notify(job_result)

    def delete(self):
        self.logger.info(f"Deleting pod {self.name}")

        attempts = 0
        max_attempts = 5
        while True:
            try:
                # Delete the specified pod by name
                self.CORE_API.delete_namespaced_pod(
                    name=self.name,
                    namespace=self.NAMESPACE,
                    body=client.V1DeleteOptions(
                        propagation_policy='Foreground'  # Ensures all related resources are also deleted
                    )
                )
            except ApiException as e:
                attempts += 1
                if attempts < max_attempts:
                    self.logger.warning(f"Attempt {attempts} of {max_attempts}")
                    time.sleep(1)
                    continue
                raise e
            else:
                break
        self.logger.info(f"{self.name} deleted")
