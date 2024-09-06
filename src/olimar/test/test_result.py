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
    SKIPPED = 6


class TestResult:
    def __init__(self, name, status: TestStatus, time, message, text, type_):
        self.name = name
        self.status = status
        self.time = time
        self.message = message
        self.text = text
        self.type = type_

    def __str__(self):
        if self.status == TestStatus.SUCCESS:
            return f"{self.name}: {self.status} in {self.time}"
        else:
            return f"{self.name}: {self.status} in {self.time}. Message: {self.message}"


class TestSuiteResult:
    def __init__(self, name, results: List[TestResult], timestamp):
        self.name = name
        self.results = results
        self.timestamp = timestamp


class TestRunResult:
    @classmethod
    def from_junit_string(cls, config, string):
        junit_xml = JUnitXml.fromstring(string)

        suite_results = []
        for suite in junit_xml:
            tests = []
            for test_case in suite:
                name = f'{test_case.classname}.{test_case.name}'
                time = test_case.time
                sout = test_case.system_out
                serr = test_case.system_err
                message = ""
                text = ""
                status = TestStatus.SUCCESS
                type_ = None

                if test_case.is_passed:
                    pass
                elif test_case.is_skipped:
                    status = TestStatus.SKIPPED
                else:
                    status = TestStatus.FAIL
                    if test_case.result:
                        message = test_case.result[0].message
                        text = test_case.result[0].text
                        type_ = test_case.result[0].type

                test = TestResult(name, status, time, message, text, type_)
                tests.append(test)

            suite_result = TestSuiteResult(suite.name, tests, suite.timestamp)
            suite_results.append(suite_result)

        return cls(config, suite_results)

    def __init__(self, config, results: List[TestSuiteResult]):
        self.config = config
        self.results = results
