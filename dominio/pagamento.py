class Pagamento:
    def __init__(self, id = "", carrinhoDeCompras = [], cliente = ""):
        self.__id = id
        self.__carrinhoDeCompras = carrinhoDeCompras
        self.__cliente = cliente
    def getId(self):
        return self.__id
    def getCarrinho(self):
        return self.__carrinhoDeCompras
    def getCliente(self):
        return self.__cliente
    def setCliente(self, cliente):
        self.__cliente = cliente
    def setCarrinho(self, carrinho):
        self.__carinho = carrinho