class Pagamento:
    def __init__(self, id = "", carrinhoDeCompras = [], endereco = endereco ):
        self.__id = id
        self.__carrinhoDeCompras = carrinhoDeCompras
        self.__endereco = endereco
    def getId(self):
        return self.__id
    def getCarrinhoDeCompras(self):
        return self.__carrinhoDeCompras
    def getEndereco(self):
        return self.__endereco
    def setEndereco(self, endereco):
        self.__endereco = endereco
    def setCarrinhoDeCompras(self, carrinho):
        self.__carinho = carrinho