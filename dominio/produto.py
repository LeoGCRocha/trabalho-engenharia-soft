class Produto:
    def __init__(self, id = "", nome = "",descricao = "",preco = "", linkImagem = "", quantidade = 0, endereco = ""):
        self.__id = id
        self.__nome = nome
        self.__descricao = descricao
        self.__preco = preco
        self.__linkImagem = linkImagem
    def getId(self):
        return self.__id
    def getNome(self):
        return self.__nome
    def getDescricao(self):
        return self.__descricao
    def getPreco(self):
        return self.__preco
    def getLinkImagem(self):
        return self.__linkImagem
    def setPreco(self, preco):
        self.__preco = preco
    def setQuantidade(self, quantidade):
        self.__quantidade = quantidade
    def getQuantidade(self):
        return self.__quantidade
    def setEndereco(self, endereco):
        self.__endereco = endereco
    def getEndereco(self):
        return self.__endereco