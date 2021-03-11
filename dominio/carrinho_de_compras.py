class CarrinhoDeCompras:
    def __init__(self, produtos = [], total = 0):
        self.__produtos = produtos
        self.__total = total
    def getProdutos(self):
        return self.__produtos
    def getTotal(self):
        return self.__total
    def setTotal(self,total):
        self.__total = total
    def setProdutos(self, produtos):
        self.__produtos = produtos