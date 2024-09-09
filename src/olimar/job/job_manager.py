import enum
import uuid
import queue
import threading
import time
from collections import deque
from datetime import datetime
from typing import List

from kubernetes import client, config
from kubernetes.stream import stream

from olimar.file_transfer.file_transfer import FileTransfer
from olimar.image.image import Image
from olimar.job.job import Job, JobWaitable
from olimar.job.job_command import JobStep
from olimar.job.job_config import JobConfig
from olimar.job.job_result import JobResult
from olimar.node.node import Node
from olimar.util.logger import Logger
from olimar.util.waitable import Waitable

# Load the kubeconfig file
config.load_kube_config()


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
        self.logger = Logger.get()

        self.delete_all_pods()
        self.lock = threading.Lock()
        self.start()

    def run(self):
        self.delete_all_pods()

        while True:
            for job in list(self._active_jobs):
                if job.status == Job.Status.NOT_STARTED:
                    job.start()
                elif job.status == Job.Status.PENDING:
                    job.check_pending()
                elif job.status == Job.Status.IDLE:
                    step = job.get_next_step()
                    if step:
                        job.start_step(step)
                    else:
                        job.cleanup()
                        self._active_jobs.remove(job)
                        self._complete_jobs.put(job)
                elif job.status == Job.Status.EXECUTING:
                    pass
                time.sleep(0.5)

    def get_nodes(self) -> List[Node]:
        node_list = self.CORE_API.list_node()
        nodes = []
        for item in node_list.items:
            # Assuming the Node class has the following fields: name, ip_address
            # Adjust these fields based on your actual Node class definition
            name = item.metadata.name
            ip_address = None
            for address in item.status.addresses:
                if address.type == 'InternalIP':
                    ip_address = address.address

            if ip_address == self.master:
                continue

            nodes.append(Node(name=name, ip_address=ip_address))
        return nodes

    def get_node(self, name) -> Node:
        for node in self.get_nodes():
            if node.name == name:
                return node
        raise KeyError(f'Node {name} not found')

    def get_jobs(self) -> List[Job]:
        raise NotImplementedError

    def delete_all_pods(self):
        # Fetch all pods in the namespace
        pods = self.CORE_API.list_namespaced_pod(namespace=self.NAMESPACE)
        for pod in pods.items:
            # Delete each pod by name
            self.CORE_API.delete_namespaced_pod(
                name=pod.metadata.name,
                namespace=self.NAMESPACE,
                body=client.V1DeleteOptions(
                    propagation_policy='Foreground'  # Ensures all related resources are also deleted
                )
            )
            self.logger.info(f"Deleted pod {pod.metadata.name}")

    def create_job(self, node: Node, image: Image, job_config: JobConfig) -> JobWaitable:
        name = f"{str(uuid.uuid4())[:6]}"
        waitable = JobWaitable()

        job = Job(name, waitable, job_config, image, node)
        self._active_jobs.append(job)
        return waitable
