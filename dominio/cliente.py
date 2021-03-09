class Cliente:
    def __init__(self, id = "", cpf = "",nome = "",email = "", senha = "",endereco = None):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__cpf = cpf
        self.__endereco = endereco
    def getNome(self):
        return self.__nome
    def getSenha(self):
        return self.__senha
    def getEmail(self):
        return self.__email
    def getId(self):
        return self.__id
    def getCpf(self):
        return self.__cpf
    def getEndereco(self):
        return self.__endereco
    def setNome(self, nome):
        self.__nome = nome
    def setCpf(self, cpf):
        self.__cpf = cpf
    def setEmail(self, email):
        self.__email = email
    def setEndereco(self, endereco):
        self.__endereco = endereco 