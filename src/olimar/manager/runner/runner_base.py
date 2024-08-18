from typing import List

from junitparser import JUnitXml

from olimar.manager.node_client.client import OlimarNodeClient, NodeCommand
from olimar.manager.runner.result import TestCaseResult, TestSuiteResult, TestResultStatus


class TestRunnerBase:
    def __init__(self, node: OlimarNodeClient, image):
        self._node = node
        self._image = image

    def run_suite(self, suite_name: str) -> List[TestSuiteResult]:
        command = NodeCommand(f"pytest -k {suite_name} "
                              f"--junitxml=/workspace/output.xml",
                              "/workspace/output.xml", 10)

        node_result = self._node.run(self._image, [command])
        result = node_result[0]

        junit_xml_string = result.artifact.get_contents()
        results = self._parse(junit_xml_string)

        return results




    @staticmethod
    def _parse(xml_string) -> List[TestSuiteResult]:
        junit_xml = JUnitXml.fromstring(xml_string)

        test_suite_results = []
        test_results = []
        for suite in junit_xml:
            for test_case in suite:
                message = ""
                text = ""
                if test_case.is_passed:
                    status = TestResultStatus.PASS
                elif test_case.is_skipped:
                    status = TestResultStatus.SKIPPED
                elif len(test_case.result) == 1:
                    result = test_case.result[0]
                    status = TestResultStatus.FAIL
                    message = result.message
                    text = result.text
                    pass
                else:
                    raise Exception

                test_case_result = TestCaseResult(test_case.name,
                                                  test_case.time,
                                                  status,
                                                  text,
                                                  message,
                                                  test_case.system_out,
                                                  test_case.system_err)
                test_results.append(test_case_result)

            test_suite_result = TestSuiteResult(suite.name, suite.hostname, suite.timestamp, test_results)
            test_suite_results.append(test_suite_result)

        return test_suite_results
