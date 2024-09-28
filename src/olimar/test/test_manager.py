from typing import List
from olimar.job.job_manager import JobManager
from olimar.test.test_run_config import TestRunConfig
from olimar.test.test_runner.test_runner_pytest import PyTestTestRunner


class TestPlan:
    def __init__(self, runs: List[TestRunConfig]):
        self.runs = runs


class TestManager:
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.job_manager = JobManager(master)
        self.runner = PyTestTestRunner(self.job_manager)

    def execute(self, test_plan: TestPlan):
        pass
