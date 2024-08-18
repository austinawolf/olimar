from test_manager.internal.docker.container_runner import ContainerRunner


def main():
    runner = ContainerRunner.from_name("example-env")
    runner.start()
    runner.exec("pytest test --junitxml=report.xml")
    report = runner.archive("/workspace/report.xml")
    print(report)
    runner.stop()


main()
