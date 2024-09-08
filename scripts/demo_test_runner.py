import threading
import time

from tabulate import tabulate

from olimar.image.image import Image
from olimar.job.job_manager import JobManager
from olimar.node.node import Node
from olimar.test.test_result import TestResult, TestRunResult
from olimar.test.test_run_config import TestRunConfig
from olimar.test.test_runner import TestRunnerBase
from olimar.test.test_runner.test_runner_pytest import PyTestTestRunner


def main():
    # Setup Test Config
    image = Image('192.168.0.250:5000', 'example-env', 'latest')

    # Setup Job Manager
    master = "192.168.0.250"
    job_manager = JobManager(master)
    nodes = job_manager.get_nodes()
    node1 = nodes[0]
    node2 = nodes[1]

    # Setup tests
    test1 = TestRunConfig('test_calculator', image, timeout=60)
    test2 = TestRunConfig('test_slow_calculator', image, timeout=60)

    # Create Test Runner
    test_runner: TestRunnerBase = PyTestTestRunner(job_manager)

    # Run Test
    run_results = []

    def run(node, test):
        result = test_runner.run(node, test)
        run_results.append(result)

    thread1 = threading.Thread(target=run, args=(node1, test1))
    thread2 = threading.Thread(target=run, args=(node2, test2))

    thread1.start()
    thread1.join()
    thread2.start()
    thread2.join()

    headers = ['Name', 'Status', 'Time']
    rows = []
    for run_result in run_results:
        for suite in run_result.results:
            for test in suite.results:
                rows.append([test.name, test.status, test.time])

    print(tabulate(rows, headers=headers, tablefmt="plain"))


main()
