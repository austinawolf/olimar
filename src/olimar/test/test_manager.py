from typing import List

from olimar.job.job_manager import JobManager
from olimar.test.test_run_config import TestRunConfig
from olimar.test.test_runner import TestRunnerBase


class TestPlan:
    def __init__(self, runs: List[TestRunConfig]):
        self.runs = runs


class TestManager:
    def __init__(self, master, runner: TestRunnerBase, job_manager: JobManager):
        self.master = master
        self.runner = runner
        self.job_manager = job_manager

    def execute(self, test_plan: TestPlan):
        pass