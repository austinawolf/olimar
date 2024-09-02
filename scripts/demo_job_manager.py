import time
from olimar.job.image import Image
from olimar.job.job_config import JobConfig
from olimar.job.job_manager import JobManager
from olimar.job.job_result import JobResult
from olimar.test.pytest_test import PyTestTest


def main():
    master = "192.168.0.250"
    test_image = Image('192.168.0.250:5000', 'example-env', 'latest')
    test_image2 = Image('localhost:5000', 'example-env', 'latest')

    test1 = PyTestTest('test_calculator')
    test2 = PyTestTest('test_slow_calculator')

    manager = JobManager(master)
    waitable1 = manager.start_job('olimar-node', test_image, test1.to_job_config())

    time.sleep(1)
    waitable2 = manager.start_job('raspberrypi2', test_image2, test2.to_job_config())

    result1: JobResult = waitable1.wait(20)
    print(result1.logs)
    result2: JobResult = waitable2.wait(40)
    print(result2.logs)


main()
