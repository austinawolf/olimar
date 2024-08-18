from junitparser import JUnitXml


from olimar.internal.docker.remote_container import RemoteContainer


def main():
    host = "192.168.47.131"

    image_path = "C:\\Users\\awolf\\dev\\other\\test-manager\\example-env\\dist\\example-env.tar"
    container = RemoteContainer.from_file(host, image_path)
    container.start()
    container.exec("ls")
    container.exec("pytest --junitxml=/workspace/output.xml")

    f = container.archive("/workspace/output.xml")
    print(f)
    container.stop()

    results = parse_junit_xml_from_string(f)
    if results:
        print("Test results:")
        for result in results:
            print(result)
    else:
        print("Failed to parse JUnit XML.")


def parse_junit_xml_from_string(xml_string):
    try:
        junit_xml = JUnitXml.fromstring(xml_string)
        test_results = []

        for suite in junit_xml:
            for test_case in suite:
                result = {
                    'name': test_case.name,
                    'classname': test_case.classname,
                    'result': test_case.result,
                    'time': test_case.time,
                    'system-out': test_case.system_out,
                    'system-err': test_case.system_err
                }
                test_results.append(result)

        return test_results
    except Exception as e:
        print(f"Error parsing JUnit XML from string: {e}")
        return None


main()
