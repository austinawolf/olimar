from olimar.job.job_config import JobConfig
from olimar.job.job_result import JobResult
from olimar.test.test_result import TestResult, TestStatus
from olimar.test.test_run_config import TestRunConfig
from olimar.test.test_runner import TestRunnerBase


class PyTestTestRunner(TestRunnerBase):
    def run(self, config: TestRunConfig) -> TestResult:
        job_config = JobConfig(f'pytest -k {config.name}')
        waitable = self.job_manager.start_job('olimar-node', config.image, job_config)
        result: JobResult = waitable.wait(config.timeout)
        return TestResult(job_config, TestStatus.SUCCESS, result.logs)

    def discover(self):
        raise NotImplementedError
