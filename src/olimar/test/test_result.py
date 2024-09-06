import enum
from typing import List

from junitparser import JUnitXml


class TestStatus(enum.Enum):
    NOT_STARTED = 0
    SUCCESS = 1
    FAIL = 2
    ERROR = 3
    TIMEOUT = 4
    BUSY = 5


class TestResult:
    def __init__(self, name, status: TestStatus, time):
        self.name = name
        self.status = status
        self.time = time

    def __str__(self):
        return f"{self.name}: {self.status} in {self.time}"


class TestSuiteResult:
    def __init__(self, name, results: List[TestResult]):
        self.results = results


class TestRunResult:
    @classmethod
    def from_junit_string(cls, config, string):
        junit_xml = JUnitXml.fromstring(string)

        suite_results = []
        for suite in junit_xml:
            tests = []
            TestSuiteResult(suite.name, suite)
            for test_case in suite:
                name = f'{test_case.classname}.{test_case.name}'
                time = test_case.time
                sout = test_case.system_out
                serr = test_case.system_err
                # message = test_case.error_message
                status = TestStatus.SUCCESS

                test = TestResult(name, status, time)
                tests.append(test)

            suite_result = TestSuiteResult(suite.name, tests)
            suite_results.append(suite_result)

        return cls(config, suite_results)

    def __init__(self, config, results: List[TestSuiteResult]):
        self.config = config
        self.results = results
