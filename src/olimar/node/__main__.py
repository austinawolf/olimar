from concurrent import futures
import grpc
from olimar.internal.grpc.build import test_runner_service_pb2
from olimar.internal.grpc.build import test_runner_service_pb2_grpc


class TestRunnerService(test_runner_service_pb2_grpc.TestRunnerServicer):

    def EchoMessage(self, request, context):
        return test_runner_service_pb2.EchoMessageReply(message=request.message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    test_runner_service_pb2_grpc.add_TestRunnerServicer_to_server(TestRunnerService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def main():
    serve()


main()
