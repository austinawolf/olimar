import time
from olimar.image.image import Image
from olimar.job.job_config import JobConfig
from olimar.job.job_manager import JobManager
from olimar.job.job_result import JobResult


def main():
    master = "192.168.0.250"
    test_image = Image('192.168.0.250:5000', 'example-env', 'latest')
    # test_image2 = Image('localhost:5000', 'example-env', 'latest')

    job_config1 = JobConfig('echo 123')

    manager = JobManager(master)
    waitable1 = manager.start_job('olimar-node', test_image, job_config1)
    # waitable2 = manager.start_job('raspberrypi2', test_image2, job_config1)

    result1: JobResult = waitable1.wait(60)
    print(result1.logs)
    # result2: JobResult = waitable2.wait(40)
    # print(result2.logs)


main()
