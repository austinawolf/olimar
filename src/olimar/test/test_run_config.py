


class TestRunConfig:
    def __init__(self, name, image, timeout: int = 60):
        self.name = name
        self.image = image
        self.timeout = timeout
