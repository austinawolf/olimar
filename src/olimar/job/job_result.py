from typing import List
from olimar.job.job_command import JobStep


class JobResult:
    def __init__(self, name, steps: List[JobStep], artifacts):
        self.name = name
        self.steps = steps
        self.artifacts = artifacts
