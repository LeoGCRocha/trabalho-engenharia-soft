class Endereco:
    def __init__(self, id = "", endereco = "", cep =""):
        self.__id = id
        self.__endereco = endereco
        self.__cep = cep
    def getId(self):
        return self.__id
    def getEndereco(self):
        return self.__endereco
    def getCEP(self):
        return self.__cep
    def setId(self, id):
        self.__id = id
    def setEndereco(self, endereco):
        self.__endereco = endereco
    def setCEP(self, cep):
        self.__cep = cep