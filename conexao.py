import psycopg2
from cliente import Cliente
from produto import Produto
class Conexao:
	def __init__(self):
		self.__con = psycopg2.connect(host='localhost', database='browrrashoes',user='postgres', password='postgres')
		self.__cur = self.__con.cursor()
	def cadastrar(self,u):
		sql = "INSERT INTO CLIENTE	(cpf,nome,email,senha)VALUES(%s,%s,%s,%s);"
		self.__cur.execute(sql, (u.getCpf(), u.getNome(),u.getEmail(), u.getSenha()))
		self.__con.commit()
	# CRUD CLIENTES
	def clientes(self):
		lista = []
		sql = "SELECT * FROM CLIENTE"
		self.__cur.execute(sql)
		rec = self.__cur.fetchall()
		for r in rec:
			c = Cliente(r[0], r[4],r[1], r[3], r[2])
			lista.append(c)
		return lista
	def getUsuario(self, id):
		lista = []
		sql = "SELECT * FROM CLIENTE WHERE ID = %s"
		self.__cur.execute(sql, str(id))
		rec = self.__cur.fetchall()
		for r in rec:
			c = Cliente(r[0], r[4],r[1], r[3], r[2])
			lista.append(c)
		return lista[0]
	def deletarUsuario(self, id):
		sql = "DELETE FROM CLIENTE WHERE id = %s"
		self.__cur.execute(sql, id)
		self.__con.commit()
	def editarCliente(self, cliente):
		sql = "UPDATE CLIENTE SET \"nome\" = %s, \"cpf\"=%s, \"email\"=%s WHERE id = %s"
		self.__cur.execute(sql,(cliente.getNome(), cliente.getCpf(), cliente.getEmail(), cliente.getId()))
		self.__con.commit()
	# CRUD PRODUTOS
	def getProdutos(self):
		lista = []
		sql = "SELECT * FROM PRODUTO"
		self.__cur.execute(sql)
		rec = self.__cur.fetchall()
		for r in rec:
			p = Produto(r[0], r[1],r[2],r[3], r[4])
			lista.append(p)
		return lista
	def cadastrar_produto(self, produto):
		sql = "INSERT INTO PRODUTO(nome,descricao,preco,link_imagem)VALUES(%s,%s,%s,%s);"
		self.__cur.execute(sql, (produto.getNome(), produto.getDescricao(),produto.getPreco(), produto.getLinkImagem()))
		self.__con.commit()
	def deletar_produto(self, id):
		sql = "DELETE FROM PRODUTO WHERE id = %s"
		self.__cur.execute(sql, id)
		self.__con.commit()
	def getProduto(self, id):
		lista = []
		sql = "SELECT * FROM PRODUTO WHERE ID = %s"
		self.__cur.execute(sql, str(id))
		rec = self.__cur.fetchall()
		for r in rec:
			p = Produto(r[0], r[1],r[2],r[3], r[4])
			lista.append(p)
		return lista[0]