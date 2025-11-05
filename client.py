import grpc
import grpcCalc_pb2
import grpcCalc_pb2_grpc
import pybreaker
import time

breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=2)

@breaker
def call_add(client, x, y):
    res = client.add(grpcCalc_pb2.args(numOne=x, numTwo=y))
    return res.num

def connect():
    channel = grpc.insecure_channel('localhost:8080')
    client = grpcCalc_pb2_grpc.apiStub(channel)
    
    # Teste normal
    print('--- Teste normal ---')
    try:
        resultado = call_add(client, 5, 3)
        print(f'5 + 3 = {resultado}')
    except pybreaker.CircuitBreakerError:
        print("Circuit Breaker ativado.")
    except Exception as e:
        print(f"Deu erro: {e}")

    # Testando as falhas
    print('\n--- Testando falhas ---')
    
    # Primeira tentativ
    try:
        print('Tentativa 1:')
        call_add(client, 10, 2)
    except pybreaker.CircuitBreakerError:
        print("Circuit Breaker ativado.")
    except Exception as e:
        print(f"Erro: {e}")

    # Segunda tentativa
    try:
        print('Tentativa 2:')
        call_add(client, 10, 2)
    except pybreaker.CircuitBreakerError:
        print("Circuit Breaker ativado.")
    except Exception as e:
        print(f"Erro: {e}")

    # Terceira tentativa (já deve estar bloqueado)
    try:
        print('Tentativa 3:')
        call_add(client, 10, 2)
    except pybreaker.CircuitBreakerError:
        print("Circuit Breaker bloqueando a chamada.")
    except Exception as e:
        print(f"Erro: {e}")

    # Espera o tempo de reset
    tempo_espera = breaker.reset_timeout + 1
    print(f'\nAguardando {tempo_espera} segundos...')
    time.sleep(tempo_espera)

    # Teste apos o reset
    print('\n--- Teste pós-reset ---')
    try:
        print('Tentando novamente:')
        resultado = call_add(client, 20, 5)
        print(f'20 + 5 = {resultado}')
    except pybreaker.CircuitBreakerError:
        print("Circuit Breaker ativado.")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    connect()