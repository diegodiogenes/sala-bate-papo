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

dict_comandos = {

}

"""
CONSTANTES PARA PRINTAR COR NO TERMINAL
"""

ON = '\033[42m'
OUT = '\033[41m'
CLOSE = '\033[0;0m'
CHANGE = '\033[43m'
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
    dict_nickname[key] = nickname.decode('utf-8')
    return CHANGE + FONT_WHITE + current_name + " alterou o nome para " + nickname + CLOSE


def client_says(key, message):
    """
    Função que recebe a chave do dicionário de nicknames e a mensagem, retorna a mensagem formatada digitada pelo cliente
    :param key:
    :param message:
    :return:
    """
    if message != 'quit':
        return FONT_BOLD + dict_nickname[key] + ' diz: ' + CLOSE + message


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


def connect_client(conn):
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
    message = ''
    while message != 'quit':
        message = conn.recv(1024).decode('utf-8')  # recebe dados do cliente
        if not message:
            break
        if client_says(conn, message) is not None:
            print(client_says(conn, message))
            write_file(client_says(conn, message))
            for client in dict_nickname:
                if client != conn:
                    client.send(client_says(conn, message).encode('utf-8'))

    print(out_client(conn, dict_nickname[conn]))
    conn.close()


def listener_clients():
    """
    aceita as conexões dos clientes
    :return:
    """
    while True:
        conn, addr = serverSocket.accept() #aceita as conexões dos clientes
        threading.Thread(target=connect_client, args=(conn,)).start()

    serverSocket.close()  # encerra o socket do servidor


# definindo dicionario para guardar ip do cliente e nickname
dict_nickname = dict()

"""
Configurando o servidor
"""
serverName = ''  # ip do servidor (em branco)
serverPort = 65001  # porta a se conectar
serverSocket = socket(AF_INET, SOCK_STREAM)  # criacao do socket TCP
serverSocket.bind((serverName, serverPort))  # bind do ip do servidor com a porta
serverSocket.listen(1)  # socket pronto para 'ouvir' conexoes
print('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))
file = open('historico.txt', 'w')
file.write('')
file.close()
listener_clients()  # Chama função para escutar os clientes

# while 1:
#     connectionSocket, addr = serverSocket.accept()  # aceita as conexoes dos clientes
#     message = connectionSocket.recv(1024)  # recebe dados do cliente
#     print(connectionSocket.fileno())
#     print(on_client(addr, message))
#     print(dict_nickname)
#     while message != 'quit':
#         print('Cliente %s enviou: %s' % (addr, message))
#         message = connectionSocket.recv(1024)
#         if not message:
#             break
#         connectionSocket.send(message)  # envia para o cliente o texto transformado
#         # print("Lista de clientes conectados: ", str(lista_addr))

