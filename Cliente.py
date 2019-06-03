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
import pickle

"""
Classes auxiliares
"""

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

"""
Classe cliente
"""


class Client(Thread):
    def __init__(self, nickname, ip_server='localhost', port=65000):
        """
        Definindo atributos da classe
        :param nickname:
        :param ip_server:
        :param port:
        """
        Thread.__init__(self)

        self.nickname = nickname
        if self.validator_nickname(nickname) is False:
            raise Exception("Nickname deve possuir até 8 caracteres e ser diferente de string vazia")

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.ip_server = ip_server
        self.port = port
        self.len_message = None
        self.command = -1
        self.message = ''
        self.online = True

    def run(self):
        """
        Definindo o método run, conectando ao socket e recebendo mensagens do servidor
        :return:
        """
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
        """
        Método que captura mensagem do teclado e envia para o servidor
        :return:
        """
        self.message = input()
        self.command, arg = self.select_command(self.message)
        header_server = self.header(self.nickname, self.command, arg)
        #header_encode = {k: v.encode("utf-8") for k,v in header_server}
        self.client_socket.send(pickle.dumps(header_server))
        if self.command == Commands.EXIT:
            self.exit_connection()

    def receive_message(self):
        """
        Método que recebe mensagens do servidor
        :return:
        """
        while self.command != Commands.EXIT:
            message_server = self.client_socket.recv(1024)
            if not message_server:
                break
            print(message_server.decode())
        self.exit_connection()

    def keep_online(self):
        return self.online

    def validator_nickname(self, nickname):
        if nickname is '':
            return False
        elif len(nickname) > 8:  # garantindo que o nickname terá no máximo 8 octetos
            self.nickname = nickname[:8]
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
        elif comando == 'sair':
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
        """
        Método que monta o cabeçalho da mensagem trocada entre cliente-servidor
        :param name:
        :param command:
        :param data:
        :return:
        """
        if len(data) > Const.SIZE_MESSAGE:  # caso a mensagem possua mais do que 80 caracteres (octetos), deverá ser truncada
            data = data[:80]

        size_header = len(data) + 4 + len(name)

        if size_header > Const.SIZE_HEADER:
            print("Tamanho da mensagem maior do que o permitido")

        dict_header = {
            "size": size_header,
            "nickname": name,
            "command": command,
            "data": data
        }

        return dict_header

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
