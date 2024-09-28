from olimar.job.job_command import JobStep
from olimar.job.job_config import JobConfig
from olimar.job.job_result import JobResult
from olimar.node.node import Node
from olimar.test.test_result import TestResult, TestStatus, TestRunResult
from olimar.test.test_run_config import TestRunConfig
from olimar.test.test_runner import TestRunnerBase


class PyTestTestRunner(TestRunnerBase):
    def run(self, node: Node, config: TestRunConfig) -> TestRunResult:
        test_step = JobStep(f'pytest -k {config.name} --capture=tee-sys -o junit_logging=out-err --junitxml=results.xml')
        result_step = JobStep(f'cat results.xml')
        job_config = JobConfig([test_step, result_step])

        waitable = self.job_manager.create_job(node, config.image, job_config)
        result: JobResult = waitable.wait(config.timeout)

        run_result = TestRunResult.from_junit_string(config, result_step.response)

        return run_result

    def discover(self):
        raise NotImplementedError
