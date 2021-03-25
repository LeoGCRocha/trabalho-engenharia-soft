class Estado:
    def __init__(self, id = "", descricao = ""):
        self.__id = id
        self.__descricao = descricao
    def getId(self):
        return self.__id
    def getDescricao(self):
        return self.__descricao 
    def setId(self, id):
        self.__id = id
    def setDescricao(self, descricao):
        self.__descricao = descricao