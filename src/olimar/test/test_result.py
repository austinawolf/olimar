import enum


class TestStatus(enum.Enum):
    NOT_STARTED = 0
    SUCCESS = 1
    FAIL = 2
    ERROR = 3
    TIMEOUT = 4
    BUSY = 5


class TestResult:
    def __init__(self, config, status, logs):
        self.config = config
        self.status = status
        self.logs = logs
