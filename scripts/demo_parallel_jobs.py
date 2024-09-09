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
    nodes = manager.get_nodes()

    waitable = manager.create_job(nodes[0], test_image, job_config)
    waitable1 = manager.create_job(nodes[1], test_image, job_config)

    result: JobResult = waitable.wait(300)
    result2: JobResult = waitable1.wait(300)

    for step in result.steps:
        print(f'Command: {step.command}, Results: {step.response}')

    for step in result2.steps:
        print(f'Command: {step.command}, Results: {step.response}')


main()
