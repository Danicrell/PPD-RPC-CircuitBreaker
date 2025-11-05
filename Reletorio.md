Relatório Técnico: Implementação de RPC com gRPC e Circuit Breaker

1. O que foi feito

Implementei um sistema de calculadora remota usando gRPC, com um mecanismo de proteção contra falhas (Circuit Breaker). A ideia era criar um servidor que faz cálculos simples e um cliente que consegue se recuperar sozinho quando o servidor fica indisponível.

2. Como fiz

2.1. Definição do contrato (grpcCalc.proto)
Criei um arquivo .proto básico definindo:

Mensagem de entrada com dois números

Mensagem de resposta com o resultado

Serviço de adição remota

2.2. Servidor (server.py)
Desenvolvi um servidor simples que:

Fica ouvindo na porta 8080

Recebe dois números e retorna a soma

Usa as classes geradas automaticamente pelo gRPC

2.3. Cliente inteligente (client.py)
Aqui foi a parte interessante - implementei o Circuit Breaker:

Configurei para abrir após 2 falhas seguidas

Tempo de reset de 2 segundos

A função de adição é protegida por esse mecanismo

3. Como testar

Preparação:

bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install grpcio grpcio-tools pybreaker

# Gerar código do gRPC
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpcCalc.proto
Execução:

Rodar o servidor: python3 server.py

Rodar o cliente: python3 client.py

4. O que aconteceu nos testes

Teste 1 - Tudo funcionando:

Cliente pede 5 + 3

Servidor responde 8

Circuit Breaker fica fechado (normal)

Teste 2 - Simulando falha:

Desliguei o servidor

Primeira tentativa: falha (mas passa)

Segunda tentativa: falha → Circuit Breaker abre

Terceira tentativa: bloqueada pelo Circuit Breaker

Resultado: cliente para de encher o servidor com requisições

Teste 3 - Recuperação:

Esperei 2 segundos (tempo de reset)

Liguei o servidor novamente

Circuit Breaker tentou uma chamada (estado meio-aberto)

Como deu certo, voltou ao normal

5. Conclusão

O Circuit Breaker mostrou ser muito útil na prática. Ele evita que o cliente fique batendo cabeça quando o servidor está com problemas, e se recupera automaticamente quando o serviço volta ao normal.

A parte legal é que o mecanismo é simples de implementar (graças à biblioteca pybreaker) mas resolve um problema real de sistemas distribuídos: como lidar com falhas temporárias sem piorar a situação.

O gRPC mostrou ser bem straightforward para criar APIs RPC, e a integração com Circuit Breaker foi tranquila. No mundo real, isso evitaria muitos problemas em produção.