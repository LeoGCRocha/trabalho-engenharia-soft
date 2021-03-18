class Pagamento:
    def __init__(self, id = "", carrinhoDeCompras = [], cliente = "", estado_produto = "Pago"):
        self.__id = id
        self.__carrinhoDeCompras = carrinhoDeCompras
        self.__cliente = cliente
        self.__estado_produto = estado_produto
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
    def getEstadoProduto(self):
        return self.__estado_produto
    def setEstadoProduto(self, estado):
        self.__estado_produto = estado