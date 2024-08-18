from olimar.manager.node_client.grpc_client import OlimarNodeClient


def main():
    # Connect
    client = OlimarNodeClient('localhost')
    client.connect()

    message = "asdf1"
    echo = client.echo(message)
    print(echo)

    client.disconnect()

    # Start Container

    # Run Command

    # Get Results

    # Show Results
    pass


if __name__ == '__main__':
    main()
