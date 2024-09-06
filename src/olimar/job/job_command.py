
class JobStep:
    def __init__(self, command):
        self.command = command
        self.response = ""
        self.is_complete = False
