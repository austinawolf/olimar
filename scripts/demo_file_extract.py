import time
from olimar.image.image import Image
from olimar.job.job_config import JobConfig
from olimar.job.job_manager import JobManager


def main():
    master = "192.168.0.250"
    test_image = Image('192.168.0.250:5000', 'example-env', 'latest')
    job = JobConfig('touch /data/file.txt')

    manager = JobManager(master)
    waitable = manager.start_job('olimar-node', test_image, job)
    result = waitable.wait(30)
    print(result.logs)


main()
