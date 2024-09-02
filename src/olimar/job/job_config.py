

class JobConfig:
    def __init__(self, command):
        self.command = command

    def get_command(self):
        return ["/bin/bash", "-c"]

    def get_args(self):
        return [self.command]
