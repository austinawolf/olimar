import time
from olimar.image.image import Image
from olimar.job.job_config import JobConfig
from olimar.job.job_manager import JobManager
from olimar.job.job_result import JobResult
from olimar.node.node import Node


def main():
    master = "192.168.0.250"
    node = Node('olimar-node', "192.168.0.173")
    test_image = Image('192.168.0.250:5000', 'example-env', 'latest')

    commands = [
        'echo 123',
        'touch file123.txt',
        'echo 123456789 > file123.txt',
        'cp file123.txt /artifacts',
        'ls /artifacts',
    ]

    artifacts = [
        '/mnt/artifacts/file123.txt',
    ]

    job_config1 = JobConfig(commands, artifacts)

    manager = JobManager(master)
    waitable1 = manager.start_job(node, test_image, job_config1)

    result1: JobResult = waitable1.wait(60)
    print(result1.logs)
    print(result1.artifacts[0].read().decode())


main()
