from dominio.cliente import *
from dominio.carrinho_de_compras import * 
class Pagamento:
    def __init__(self, id = "", carrinhoDeCompras = CarrinhoDeCompras(), cliente = Cliente(), estado_produto = "Pago"):
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
        self.__carrinhoDeCompras = carrinho
    def getEstadoProduto(self):
        return self.__estado_produto
    def setEstadoProduto(self, estado):
        self.__estado_produto = estado