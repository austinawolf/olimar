from olimar.image.image import Image
from olimar.job.job_command import JobStep
from olimar.job.job_config import JobConfig
from olimar.job.job_manager import JobManager
from olimar.job.job_result import JobResult
from olimar.util.logger import Logger


def main():
    Logger.configure()

    master = "192.168.0.250"
    test_image = Image('192.168.0.250:5000', 'example-env', 'latest')

    steps = [
        JobStep('echo 123'),
        JobStep('touch file123.txt'),
        JobStep('echo 123456789 > file123.txt'),
        JobStep('cp file123.txt /artifacts'),
        JobStep('ls /artifacts'),
    ]

    job_config = JobConfig(steps)

    manager = JobManager(master)
    node = manager.get_node('olimar-node')
    node2 = manager.get_node('olimar-node2')

    waitable = manager.create_job(node, test_image, job_config)
    waitable = manager.create_job(node, test_image, job_config)

    result: JobResult = waitable.wait(300)

    for step in result.steps:
        print(f'Command: {step.command}, Results: {step.response}')


main()
