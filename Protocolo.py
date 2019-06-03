# Classe do protocolo de comunicação entre cliente e servidor


class Protocol:
    def __init__(self, ip_orig=None, ip_dest=None, nickname=None, comando=-1, mensagem=''):
        self.ip_orig = ip_orig
        self.ip_dest = ip_dest
        self.nickname = nickname
        self.comando = comando
        self.mensagem = mensagem

    def sendFrame(self):

