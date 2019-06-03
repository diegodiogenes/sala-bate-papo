# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTORES: DIEGO BRUNO DANTAS DIÓGENES
#          DOUGLAS DE SOUZA CARVALHO
# SCRIPT: Cliente de sockets TCP modificado para enviar texto minusculo ao servidor e aguardar resposta em maiuscula
#

# importacao das bibliotecas
from socket import *
import threading

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

# definicao das variaveis
serverName = 'localhost' # ip do servidor
serverPort = 65000  # porta a se conectar
clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor
message = ''
nickname = input('Digite o seu nickname: ')
clientSocket.send(nickname.encode('utf-8'))


def send_message(message):
    while message != 'quit':
        modifiedSentence = clientSocket.recv(1024)
        print(modifiedSentence.decode('utf-8'))
    return 0


while message != 'quit':
    clientSocket.send(message.encode('utf-8'))
    threading.Thread(target=send_message, args=(message,)).start()
    message = input()


clientSocket.send(message.encode('utf-8'))
clientSocket.close()
