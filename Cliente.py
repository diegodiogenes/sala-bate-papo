# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTORES: DIEGO BRUNO DANTAS DIÓGENES
#          DOUGLAS DE SOUZA CARVALHO
# SCRIPT: Cliente de sockets TCP modificado para enviar texto minusculo ao servidor e aguardar resposta em maiuscula
#

# importacao das bibliotecas
from socket import *

# definicao das variaveis
serverName = 'localhost' # ip do servidor
serverPort = 65001 # porta a se conectar
clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor
message = ''
nickname = input('Digite o seu nickname: ')
clientSocket.send(nickname.encode('utf-8'))

while message != 'quit':
    message = input('Digite sua mensagem: ')
    clientSocket.send(message.encode('utf-8'))
    modifiedSentence = clientSocket.recv(1024)
    print('O servidor (\'%s\', %d) respondeu com: %s' % (serverName, serverPort, modifiedSentence))

clientSocket.send(message.encode('utf-8'))
clientSocket.close()
