from olimar.manager.node_client.client import OlimarNodeClient, NodeCommand


def main():
    host = "192.168.47.131"
    image_path = "C:\\Users\\awolf\\dev\\other\\test-manager\\example-env\\dist\\example-env.tar"

    # Read Image
    f = open(image_path, 'rb')
    image = f.read()
    f.close()

    node = OlimarNodeClient(host)

    results = node.run(image,
                       [
                           NodeCommand("pytest -k test_calculator --junitxml=/workspace/output.xml",
                                       "/workspace/output.xml", 10),
                           NodeCommand("pytest -k test_slow_calculator --junitxml=/workspace/output.xml",
                                       "/workspace/output.xml", 10),
                       ])



main()
