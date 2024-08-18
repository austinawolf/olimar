import logging
from olimar.manager.node_client.client import OlimarNodeClient
from olimar.manager.runner.runner_base import TestRunnerBase


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


def main():
    setup_logger()

    # host = "192.168.47.131"
    # image_path = "C:\\Users\\awolf\\dev\\other\\test-manager\\example-env\\dist\\example-env.tar"

    host = "192.168.0.172"
    image_path = "C:\\Users\\awolf\\dev\\other\\test-manager\\example-env\\dist\\example-env_arm64.tar"

    # Read Image
    f = open(image_path, 'rb')
    image = f.read()
    f.close()

    node = OlimarNodeClient(host)

    test_runner = TestRunnerBase(node, image)

    results = test_runner.run_suite("test_calculator")
    results += test_runner.run_suite("test_slow_calculator")

    for result in results:
        print(result)


main()
