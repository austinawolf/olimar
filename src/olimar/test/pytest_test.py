from olimar.job.job_config import JobConfig


class PyTestTest:
    def __init__(self, test_suite):
        self.test_suite = test_suite

    def to_job_config(self) -> JobConfig:
        return JobConfig(f'pytest -k {self.test_suite}')
