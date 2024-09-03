from olimar.image.image import Image
from olimar.job.job_manager import JobManager
from olimar.test.test_result import TestResult
from olimar.test.test_run_config import TestRunConfig
from olimar.test.test_runner import TestRunnerBase
from olimar.test.test_runner.test_runner_pytest import PyTestTestRunner


def main():
    # Setup Test Config
    image = Image('192.168.0.250:5000', 'example-env', 'latest')

    run_configs = [
        TestRunConfig('test_calculator', image, timeout=60),
        TestRunConfig('test_calculator', image, timeout=60),
    ]

    # Setup Job Manager
    master = "192.168.0.250"
    job_manager = JobManager(master)

    # Create Test Manager
    test_runner: TestRunnerBase = PyTestTestRunner(job_manager)

    # Run Test
    for run_config in run_configs:
        result: TestResult = test_runner.run(run_config)
        print(result.logs)


main()
