import grpc
import test_pb2
import test_pb2_grpc

from random import randint

def test(stub):
    empty_request = test_pb2.EmptyRequest()
    test_response = stub.Test(empty_request)
    return test_response

def hello_name(stub, name):
    hello_request = test_pb2.HelloRequest(name=name)
    hello_response = stub.HelloName(hello_request)
    return hello_response

def hello_many_times(stub, name):
    hello_request = test_pb2.HelloRequest(name=name)
    hello_responses = stub.HelloManyTimes(hello_request)
    return hello_responses

def weird_name_requests():
    for i in range(0, 10):
        yield test_pb2.HelloRequest(name="123 de Oliveira {}".format(i))

def hello_to_a_bunch_of_people(stub):
    hello_request = weird_name_requests()
    hello_responses = stub.HelloToABunchOfPeople(hello_request)
    return hello_responses

def hello_all(stub):
    hello_request = weird_name_requests()
    hello_responses = stub.HelloAll(hello_request)
    return hello_responses

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = test_pb2_grpc.TestStub(channel)

        print('---------- Test ----------')
        print(test(stub))

        print('---------- HelloName ----------')
        print(hello_name(stub, 'Eduardo'))

        print('---------- HelloManyTimes ----------')
        hello_responses = hello_many_times(stub, 'Eduardo')
        for hello_response in hello_responses:
            print(hello_response)

        print('---------- HelloToABunchOfPeople ----------')
        print(hello_to_a_bunch_of_people(stub))
        
        print('---------- HelloAll ----------')
        hello_responses = hello_all(stub)
        for hello_response in hello_responses:
            print(hello_response)

if __name__ == '__main__':
    main()