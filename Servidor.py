# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: DIEGO BRUNO DANTAS DIÓGENES
#        DOUGLAS DE SOUZA CARVALHO
# SCRIPT: Servidor de sockets TCP modificado para receber texto minusculo do cliente enviar resposta em maiuscula
#

# importacao das bibliotecas
from socket import *  # sockets
import threading

"""
CONSTANTES
"""

ON = '\033[42m'
OUT = '\033[0;0m'
CLOSE = '\033[0;0m'
CHANGE = '\033[41m'
FONT_WHITE = '\033[37m'

"""
FUNÇÕES
"""

def on_client(key, nickname):
    """
    Adiciona o IP do cliente como chave de um dicionário e o seu nickname como sendo o valor, retorna uma string com
    fundo verde informando que o usuário entrou na sala
    :param key:
    :param nickname:
    :return:
    """
    dict_nickname[key] = nickname.decode('utf-8')
    return ON + FONT_WHITE + nickname.decode('utf-8') + ' acabou de entrar na sala' + CLOSE


def out_client(key, nickname):
    """
    Remove do dicionário de nicknames o cliente que saiu da sala de bate papo, retorna uma string em vermelho informando
    o nickname do cliente que acabou de deixar a sala
    :param key:
    :param nickname:
    :return:
    """
    dict_nickname.pop(key, nickname)
    return OUT + FONT_WHITE + nickname.decode('utf-8') + " acabou de deixar a sala" + CLOSE


def change_nick(key, nickname):
    """
    Altera o nick name do cliente no dicionario de nicknames e informa na tela do terminal que o nome foi alterado
    :param key:
    :param nickname:
    :return:
    """
    current_name = dict_nickname[key]
    dict_nickname[key] = nickname.decode('utf-8')
    return CHANGE + FONT_WHITE + current_name + " alterou o nome paraa " + nickname + CLOSE

def listener_clients():
    while True:
        conn, addr = serverSocket.accept() #aceita as conexões dos clientes
        

# definindo dicionario para guardar ip do cliente e nickname
dict_nickname = dict()

"""
Configurando o servidor
"""
serverName = ''  # ip do servidor (em branco)
serverPort = 65000  # porta a se conectar
serverSocket = socket(AF_INET, SOCK_STREAM)  # criacao do socket TCP
serverSocket.bind((serverName, serverPort))  # bind do ip do servidor com a porta
serverSocket.listen(1)  # socket pronto para 'ouvir' conexoes
print('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))

while 1:
    connectionSocket, addr = serverSocket.accept()  # aceita as conexoes dos clientes
    message = connectionSocket.recv(1024)  # recebe dados do cliente
    print(connectionSocket.fileno())
    print(on_client(addr, message))
    print(dict_nickname)
    while message != 'quit':
        print('Cliente %s enviou: %s' % (addr, message))
        message = connectionSocket.recv(1024)
        if not message:
            break
        connectionSocket.send(message)  # envia para o cliente o texto transformado
        # print("Lista de clientes conectados: ", str(lista_addr))
    connectionSocket.close()  # encerra o socket com o cliente
    serverSocket.close()  # encerra o socket do servidor
