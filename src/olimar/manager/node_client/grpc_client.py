import grpc
from olimar.internal.grpc.build import test_runner_service_pb2
from olimar.internal.grpc.build import test_runner_service_pb2_grpc


# def run():
#     with grpc.insecure_channel('localhost:50051') as channel:
#         stub = test_runner_service_pb2_grpc.TestRunnerStub(channel)
#         for i in range(10):
#             response = stub.EchoMessage(test_runner_service_pb2.EchoMessageRequest(message=f'Test: {i}'))
#             print(response.message)


class OlimarGrpcNodeClient:
    GRPC_PORT = 50051

    def __init__(self, host):
        self._host = host
        self._is_connected = False
        self._channel = None

    def is_connected(self) -> None:
        return self._channel is not None

    @property
    def _stub(self):
        return test_runner_service_pb2_grpc.TestRunnerStub(self._channel)

    def connect(self):
        if self.is_connected():
            raise Exception

        self._channel = grpc.insecure_channel(f'{self._host}:{self.GRPC_PORT}')

    def echo(self, message):
        response = self._stub.EchoMessage(test_runner_service_pb2.EchoMessageRequest(message=message))
        return response.message

    def disconnect(self):
        self._channel.close()
        self._channel = None
