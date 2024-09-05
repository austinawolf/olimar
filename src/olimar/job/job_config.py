


class JobConfig:
    def __init__(self, commands, artifacts):
        self.commands = commands
        self.artifacts = artifacts

    def get_command(self):
        return ["/bin/bash", "-c"]

    def get_args(self):
        raise NotImplementedError

    def add_artifact(self, artifact: str):
        self.artifacts.append(artifact)
