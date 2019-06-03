# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTORES: DIEGO BRUNO DANTAS DIÓGENES
#          DOUGLAS DE SOUZA CARVALHO
# SCRIPT: Cliente de sockets TCP modificado para criação de uma sala de bate-papo
#

# importacao das bibliotecas
from socket import *
from threading import Thread


class Commands:
    PUBLIC = 0
    PRIVATE = 1
    NAME = 2
    LIST = 3
    EXIT = 4


class Const:
    SIZE_HEADER = 99
    SIZE_NICK = 8
    SIZE_COMMAND = 8
    SIZE_MESSAGE = 80


class Client(Thread):
    def __init__(self, nickname, ip_server='localhost', port=65000):
        Thread.__init__(self)
        if self.validator_nickname(nickname) is False:
            raise Exception("Nickname deve possuir até 8 caracteres e ser diferente de string vazia")

        # garantindo que o nickname terá extamente 8 octetos
        if len(nickname) < 8:
            nickname += (8 - len(nickname)) * ' '

        self.nickname = nickname
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.ip_server = ip_server
        self.port = port
        self.len_message = None
        self.command = -1
        self.message = ''
        self.online = True

    def run(self):
        try:
            self.client_socket.connect((self.ip_server, self.port))
        except:
            print("Falha ao manter comunicação com o servidor")
            self.exit_connection()
            exit()

        self.client_socket.send(self.nickname.encode('utf-8'))
        while self.online is True:
            self.receive_message()
        exit()

    def send_message(self):
        self.message = input()
        self.command, arg = self.select_command(self.message)
        self.client_socket.send(self.message.encode())
        if self.command == Commands.EXIT:
            self.exit_connection()

    def receive_message(self):
        while self.command != Commands.EXIT:
            message_server = self.client_socket.recv(1024)
            if not message_server:
                break
            print(message_server.decode())
        self.exit_connection()

    def keep_online(self):
        return self.online

    @staticmethod
    def validator_nickname(nickname):
        if len(nickname) > 8 or nickname is '':
            return False
        return True

    @staticmethod
    def select_command(message):
        comando = Commands.PUBLIC  # por padrão a conexao do chat é pública e espera-se que o usuario digitou uma mensagem

        if message.find('(') is -1:  # caso não seja encontrado parentese na string, é apenas uma mensagem normal
            return comando, message
        elif message.find(
                ')') is -1:  # caso seja encontrado um parentese, mas nao o seu fechamento, é também uma mensagem
            return comando, message

        split_string = message.split('(')
        comando = split_string[0]
        arg = split_string[1].split(')')[0]

        if comando == 'listar':
            comando = Commands.LIST
        elif comando == 'exit':
            comando = Commands.EXIT
        elif comando == 'nome':
            comando = Commands.NAME
        elif comando == 'privado':
            comando = Commands.PRIVATE
        else:
            print("Comando não encontrado")
            exit()

        return comando, arg

    @staticmethod
    def header(name, command, data):
        if len(data) > 80: # caso a mensagem possua mais do que 80 caracteres (octetos), não será enviado
            exit()
        else:
            size_header = len(data) + len(command) + len(name)

    def exit_connection(self):
        self.client_socket.close()
        self.online = False


# definicao das variaveis


# dict_protocol = dict()
serverName = 'localhost'  # ip do servidor
serverPort = 65000  # porta a se conectar
# clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
# clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor
message = ''
nickname = input('Digite o seu nickname: ')

cliente = Client(nickname=nickname, ip_server=serverName, port=serverPort)
cliente.start()

while cliente.keep_online() is True:
    cliente.send_message()
print("Cliente desconectado, até a próxima!")
