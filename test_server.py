from concurrent import futures
from random import randint

import grpc
import test_pb2
import test_pb2_grpc

class TestServicer():
    def Test(self, request, context):
        return test_pb2.TestResponse(test="Test")

    def HelloName(self, request, context):
        name = request.name
        return test_pb2.HelloResponse(hello="Hello {}!".format(name))

    def HelloManyTimes(self, request, context):
        name = request.name
        for i in range(0, randint(0, 20)):
            yield test_pb2.HelloResponse(hello="Hello {} #{}!".format(name, i + 1))

    def HelloToABunchOfPeople(self, request_iterator, context):
        names = []
        for request in request_iterator:
            names.append(request.name)
        return test_pb2.HelloResponse(hello="Hello {}!".format(', '.join(names)))

    def HelloAll(self, request_iterator, context):
        for request in request_iterator:
            yield test_pb2.HelloResponse(hello="Hello {}!".format(request.name))

def serve(): 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_TestServicer_to_server(TestServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def main():
    serve()

if __name__ == '__main__':
    main()
