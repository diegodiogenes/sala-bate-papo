# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: DIEGO BRUNO DANTAS DIÓGENES
#        DOUGLAS DE SOUZA CARVALHO
# SCRIPT: Servidor de sockets TCP modificado para criação de um bate-papo, recebe mensagens, envia em broadcast e gerencia conexões
#

# importacao das bibliotecas
from socket import *  # sockets
import threading
import pickle


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
CONSTANTES PARA PRINTAR COR NO TERMINAL
"""

ON = '\033[42m'
OUT = '\033[41m'
CLOSE = '\033[0;0m'
CHANGE = '\033[45m'
FONT_WHITE = '\033[37m'
FONT_BOLD = '\033[1m'

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
    information_on_client = ON + FONT_WHITE + nickname.decode('utf-8') + ' acabou de entrar na sala' + CLOSE
    dict_nickname[key] = nickname.decode('utf-8')
    return information_on_client


def out_client(key, nickname):
    """
    Remove do dicionário de nicknames o cliente que saiu da sala de bate papo, retorna uma string em vermelho informando
    o nickname do cliente que acabou de deixar a sala
    :param key:
    :param nickname:
    :return:
    """
    dict_nickname.pop(key, nickname)
    information_client_out = OUT + FONT_WHITE + nickname + " acabou de deixar a sala" + CLOSE
    for client in dict_nickname:
        if client != key:
            client.send(information_client_out.encode('utf-8'))
    return information_client_out


def change_nick(key, nickname):
    """
    Altera o nick name do cliente no dicionario de nicknames e informa na tela do terminal que o nome foi alterado
    :param key:
    :param nickname:
    :return:
    """
    current_name = dict_nickname[key]
    dict_nickname[key] = nickname
    return CHANGE + FONT_WHITE + current_name + " alterou o nome para " + nickname + CLOSE


def client_says(key, message):
    """
    Função que recebe a chave do dicionário de nicknames e a mensagem, retorna a mensagem formatada digitada pelo cliente
    :param key:
    :param message:
    :return:
    """
    if message != 'sair':
        return FONT_BOLD + dict_nickname[key] + ' diz: ' + CLOSE + message


def client_list(conn, addr):
    """
    Função que lista todos os clientes conectados
    Cabe melhorias
    1) listar Nome, ip, portas
    """
    string = 'Os clientes conectados são: \n'
    conn.send(string.encode('utf-8'))
    for client in dict_nickname:
        client_list = dict_nickname[client] + ', de ip: ' + str(addr[0]) + ' na porta: ' + str(addr[1]) + '\n'
        conn.send(client_list.encode('utf-8'))


def exit_connection(conn):
    client_disconnect = out_client(conn, dict_nickname[conn])
    write_file(client_disconnect)
    print(client_disconnect)


def send_broadcast(conn, message):
    for client in dict_nickname:
        if client != conn:
            client.send(client_says(conn, message).encode('utf-8'))


def validation_header(header, conn, addr, nickname):
    """
    Função que recebe o cabeçalho e irá verificar o comando digitado pelo cliente
    :param header:
    :param conn:
    :param addr:
    :param nickname:
    :return:
    """
    command = header['command']

    if command == Commands.LIST:
        client_list(conn, addr)
    elif command == Commands.NAME:
        nick_changed = change_nick(conn, header['data'])
        print(nick_changed)
        write_file(nick_changed)
        for client in dict_nickname:
            if client != conn:
                client.send(nick_changed.encode('utf-8'))
    elif command == Commands.EXIT:
        exit_connection(conn)
    elif command == Commands.PRIVATE:
        print("Comando ainda não implementado")
    else:
        if client_says(conn, header['data']) is not None:
            message_broadcast = client_says(conn, header['data'])
            print(message_broadcast)
            write_file(message_broadcast)
            send_broadcast(conn, header['data'])


def write_file(message):
    """
    Função que tem objetivo de gravar no arquivo historico.txt que registra o historico da conversa do bate-papo
    :param message:
    :return:
    """
    f = open('historico.txt', 'a')
    f.write(message + '\n')
    f.close()


def send_history(conn):
    f = open('historico.txt', 'r')
    historico = f.read()
    conn.send(historico.encode('utf-8'))
    f.close()


def connect_client(conn, addr):
    """
    Mantém a conexão com os clientes, recebe as mensagens e envie em broadcast
    :param conn:
    :return:
    """
    nickname = conn.recv(1024)
    print(on_client(conn, nickname))
    for client in dict_nickname:
        if client != conn:
            client.send(on_client(conn, nickname).encode('utf-8'))
    send_history(conn)
    write_file(on_client(conn, nickname))
    message = {'command': '', 'data': ''}
    while message['command'] != Commands.EXIT:
        message = conn.recv(1024)  # recebe dados do cliente
        message = pickle.loads(message)
        if not message:
            break
        validation_header(message, conn, addr, nickname)

    conn.close()


def listener_clients():
    """
    aceita as conexões dos clientes
    :return:
    """
    while True:
        conn, addr = serverSocket.accept()  # aceita as conexões dos clientes
        threading.Thread(target=connect_client, args=(conn, addr,)).start()

    serverSocket.close()  # encerra o socket do servidor


# definindo dicionario para guardar informações do socket do cliente e nickname
dict_nickname = dict()

# definindo dicionario para guardar ip/porta do cliente e nickname
dict_ip_nickname = dict()

"""
Configurando o servidor
"""
serverName = ''  # ip do servidor (em branco)
serverPort = 65000  # porta a se conectar
serverSocket = socket(AF_INET, SOCK_STREAM)  # criacao do socket TCP
serverSocket.bind((serverName, serverPort))  # bind do ip do servidor com a porta
serverSocket.listen(1)  # socket pronto para 'ouvir' conexoes
print('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))
file = open('historico.txt', 'w')
file.write('')
file.close()
listener_clients()  # Chama função para escutar os clientes
