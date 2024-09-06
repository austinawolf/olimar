from typing import List
from olimar.job.job_command import JobStep


class JobConfig:
    def __init__(self, steps: List[JobStep]):
        self.steps = steps
        self.artifacts = []
