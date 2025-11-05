import grpc
import time
from concurrent import futures
import grpcCalc_pb2
import grpcCalc_pb2_grpc


def serve():
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpcCalc_pb2_grpc.add_apiServicer_to_server(CalculatorServicer(), grpc_server)
    grpc_server.add_insecure_port('[::]:8080')
    print("Servidor gRPC iniciado na porta 8080...")
    grpc_server.start()
    grpc_server.wait_for_termination()


class CalculatorServicer(grpcCalc_pb2_grpc.apiServicer):

    def add(self, request, context):
        # Simulação de falha para testar o Circuit Breaker
        # if time.time() % 10 < 3:
        #     context.set_code(grpc.StatusCode.UNAVAILABLE)
        #     context.set_details('Serviço temporariamente indisponível')
        #     return grpcCalc_pb2.result(num=0)

        return grpcCalc_pb2.result(num=(request.numOne + request.numTwo))


if __name__ == '__main__':
    serve()