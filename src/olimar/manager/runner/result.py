from enum import Enum
from typing import List


class TestResultStatus(Enum):
    PASS = 0
    FAIL = 1
    ERROR = 2
    SKIPPED = 3
    TIMEOUT = 4


class TestCaseResult:
    def __init__(self, name, time, status, text, message, sout, serr):
        self.name = name
        self.time = time
        self.status = status
        self.text = text
        self.message = message
        self.sout = sout
        self.serr = serr


class TestSuiteResult:
    def __init__(self, name, hostname, timestamp, cases: List[TestCaseResult]):
        self.name = name
        self.hostname = hostname
        self.timestamp = timestamp
        self.cases = cases

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Name: {self.name}, " \
               f"Hostname: {self.hostname}, " \
               f"Timestamp: {self.timestamp}, " \
               f"Pass: {len(self.passes)} / {self.test_count}"

    @property
    def test_count(self):
        return len([case for case in self.cases if case.status])

    @property
    def errors(self):
        return [case for case in self.cases if case.status == TestResultStatus.ERROR]

    @property
    def failures(self):
        return [case for case in self.cases if case.status == TestResultStatus.FAIL]

    @property
    def skipped(self):
        return [case for case in self.cases if case.status == TestResultStatus.SKIPPED]

    @property
    def passes(self):
        return [case for case in self.cases if case.status == TestResultStatus.PASS]

    @property
    def time(self):
        return sum([case.time for case in self.cases])
