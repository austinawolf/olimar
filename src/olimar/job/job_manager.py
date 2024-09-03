import queue
import threading
import time
from collections import deque
from datetime import datetime

from kubernetes import client, config
from kubernetes.stream import stream

from olimar.image.image import Image
from olimar.job.job_config import JobConfig
from olimar.job.job_result import JobResult
from olimar.util.waitable import Waitable

# Load the kubeconfig file
config.load_kube_config()


class JobWaitable(Waitable):
    def __init__(self, name):
        super().__init__()
        self.name = name


class JobManager(threading.Thread):
    NAMESPACE = 'default'
    BATCH_API = client.BatchV1Api()
    CORE_API = client.CoreV1Api()

    def __init__(self, master: str):
        super().__init__()
        self.master = master
        self._active_jobs = deque()
        self._complete_jobs = queue.Queue(maxsize=50)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            for job in list(self._active_jobs):
                job: JobWaitable = job
                job_status = self.BATCH_API.read_namespaced_job_status(job.name, self.NAMESPACE)
                if job_status.status.active:
                    print(f'{job.name} is active')
                elif job_status.status.failed:
                    print(f'{job.name} failed')
                    self._active_jobs.remove(job)
                elif job_status.status.succeeded:
                    self._active_jobs.remove(job)
                    print(f'{job.name} succeeded')
                    logs = self.get_logs(job.name)
                    result = JobResult(job.name, logs)
                    job.notify(result)
                else:
                    print(f'{job.name} state unknown')
            time.sleep(1)

    def get_logs(self, job_name):
        pod_list = self.CORE_API.list_namespaced_pod(self.NAMESPACE, label_selector=f"job-name={job_name}")
        pod_name = pod_list.items[0].metadata.name
        # Retrieve the logs from the pod
        logs = self.CORE_API.read_namespaced_pod_log(pod_name, self.NAMESPACE)
        return logs

    def start_job(self, node_name: str, image: Image, job_config: JobConfig):
        datetime_str = datetime.now().strftime('%Y%m%d-%H%M%S')
        job_name = f"job-{datetime_str}"

        container = client.V1Container(
            name="my-container",
            image=image.to_link(),
            command=job_config.get_command(),
            args=job_config.get_args(),
            volume_mounts=[
                client.V1VolumeMount(
                    name="my-volume",
                    mount_path="/data"
                )
            ]
        )

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"job-name": job_name}),
            spec=client.V1PodSpec(
                containers=[container],
                restart_policy="Never",
                node_selector={"kubernetes.io/hostname": node_name},  # This assigns the pod to a specific node
                volumes=[
                    client.V1Volume(
                        name="my-volume",
                        host_path=client.V1HostPathVolumeSource(
                            path='/mnt/data',
                            type='DirectoryOrCreate'
                        ),
                    )
                ],
            )
        )

        job_spec = client.V1JobSpec(
            template=template,
            backoff_limit=4
        )

        # Define the job
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=job_name),
            spec=job_spec
        )

        self.BATCH_API.create_namespaced_job(
            namespace=self.NAMESPACE,
            body=job
        )

        waitable = JobWaitable(job_name)

        self._active_jobs.append(waitable)
        return waitable

    def _get_pod_name_by_job(self, job_name: str) -> str:
        pods = self.CORE_API.list_namespaced_pod(
            namespace=self.NAMESPACE,
            label_selector=f"job-name={job_name}"
        ).items
        return pods[0].metadata.name if pods else None

    def _extract_file_from_pod(self, pod_name: str, src_path: str, dest_path: str):
        exec_command = ['tar', 'cf', '-', src_path]
        resp = stream(self.CORE_API.connect_get_namespaced_pod_exec,
                      pod_name,
                      self.NAMESPACE,
                      container='my-container',
                      command=exec_command,
                      stderr=True, stdin=False,
                      stdout=True, tty=False)

        with open(dest_path, 'wb') as f:
            f.write(resp)
