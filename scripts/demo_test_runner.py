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

    run_configs = [
        TestRunConfig('test_calculator', image, timeout=60),
        TestRunConfig('test_slow_calculator', image, timeout=60),
    ]

    # Setup Job Manager
    master = "192.168.0.250"
    job_manager = JobManager(master)

    # Create Test Manager
    test_runner: TestRunnerBase = PyTestTestRunner(job_manager)

    # Run Test
    run_results = []
    for run_config in run_configs:
        run_result: TestRunResult = test_runner.run(run_config)
        run_results += [run_result]

    for run in run_results:
        for suite in run.results:
            for test in suite.results:
                print(test)



main()
