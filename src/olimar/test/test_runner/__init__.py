from olimar.job.job_manager import JobManager
from olimar.test.test_result import TestRunResult
from olimar.test.test_run_config import TestRunConfig


class TestRunnerBase:
    def __init__(self, job_manager: JobManager):
        self.job_manager = job_manager

    def run(self, config: TestRunConfig) -> TestRunResult:
        raise NotImplementedError

    def discover(self):
        raise NotImplementedError
