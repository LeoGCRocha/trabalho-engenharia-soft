import psycopg2
from dominio.cliente import Cliente
from dominio.produto import Produto
from dominio.estado import Estado
from dominio.endereco import Endereco
from dominio.carrinho_de_compras import CarrinhoDeCompras
from dominio.pagamento import Pagamento
class Conexao:
	def __init__(self):
		self.__con = psycopg2.connect(host='localhost', database='browrrashoes',user='postgres', password='postgres')
		self.__cur = self.__con.cursor()
	# CRUD
	def getEstadoPorId(self, id):
		sql = "SELECT * FROM estado_pedido WHERE id = %s"
		self.__cur.execute(sql, str(id))
		rec = self.__cur.fetchone()
		estado = Estado(rec[0],rec[1])
		return estado
	def cadastrar(self,u):
		sql = "INSERT INTO CLIENTE	(cpf,nome,email,senha)VALUES(%s,%s,%s,%s);"
		self.__cur.execute(sql, (u.getCpf(), u.getNome(),u.getEmail(), u.getSenha()))
		self.__con.commit()	
	def clientes(self):
		lista = []
		sql = "SELECT * FROM CLIENTE"
		self.__cur.execute(sql)
		rec = self.__cur.fetchall()
		for r in rec:
			c = Cliente(r[0], r[4],r[1], r[3], r[2])
			endereco = self.pegar_endereco_por_id_cliente(r[0])
			c.setEndereco(endereco)
			lista.append(c)
		return lista
	def get_cliente_por_id(self, id):
		lista = []
		sql = "SELECT * FROM CLIENTE WHERE ID = %s"
		self.__cur.execute(sql, str(id))
		rec = self.__cur.fetchall()
		for r in rec:
			c = Cliente(r[0], r[4],r[1], r[3], r[2])
			endereco = self.pegar_endereco_por_id_cliente(r[0])
			c.setEndereco(endereco)
			lista.append(c)
		return lista[0]
	def deletar_cliente_por_id(self, id):
		sql = "DELETE FROM CLIENTE WHERE id = %s"
		self.__cur.execute(sql, id)
		self.__con.commit()
	def editarCliente(self, cliente):
		sql = "UPDATE CLIENTE SET \"nome\" = %s, \"cpf\"=%s, \"email\"=%s WHERE id = %s"
		self.__cur.execute(sql,(cliente.getNome(), cliente.getCpf(), cliente.getEmail(), cliente.getId()))
		self.__con.commit()
	# Criar, Deletar, Editar e Pegar Enderecos
	def pegar_endereco_por_id_cliente(self, id_cliente):
		sql = "SELECT * FROM ENDERECO WHERE cliente_id = %s"
		self.__cur.execute(sql, str(id_cliente))
		rec = self.__cur.fetchall()
		if(len(rec) == 0):
			return None
		else:
			obj = rec[0]
			endereco = Endereco(obj[0], obj[1], obj[2])
			return endereco
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
	def getProdutosPreco(self):
		lista = []
		sql = "SELECT * FROM PRODUTO ORDER BY PRECO"
		self.__cur.execute(sql)
		rec = self.__cur.fetchall()
		for r in rec:
			p = Produto(r[0], r[1],r[2],r[3], r[4])
			lista.append(p)
		return lista
	def getProdutosNome(self):
		lista = []
		sql = "SELECT * FROM PRODUTO ORDER BY NOME"
		self.__cur.execute(sql)
		rec = self.__cur.fetchall()
		for r in rec:
			p = Produto(r[0], r[1],r[2],r[3], r[4])
			lista.append(p)
		return lista
	def getProdutosBusca(self, atributo):
		lista = []
		atributo = "%"+ atributo +"%"
		sql = "SELECT * FROM PRODUTO where nome like \'"+atributo+"\'"
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
		sql = "SELECT * FROM PAGAMENTOPRODUTO WHERE produto_id = %s"
		self.__cur.execute(sql, str(id))
		rec = self.__cur.fetchall()
		if len(rec) == 0:
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
	def editar_produto(self, produto):
		sql = "UPDATE PRODUTO SET \"nome\" = %s, \"link_imagem\"=%s, \"descricao\"=%s, \"preco\"=%s WHERE id = %s"
		self.__cur.execute(sql,(produto.getNome(), produto.getLinkImagem(), produto.getDescricao(), produto.getPreco(), produto.getId()))
		self.__con.commit()
	# CADASTRAR ENDERECO
	def cadastrar_endereco(self, cliente):
		sql = "INSERT INTO ENDERECO(endereco,cep,cliente_id)VALUES(%s,%s,%s);"
		endereco = cliente.getEndereco()
		self.__cur.execute(sql, (endereco.getEndereco(), endereco.getCEP(),cliente.getId()))
		self.__con.commit()
	# FINALIZAR PAGAMENTO
	def finalizar_pagamento(self, pagamento):
		carrinho = pagamento.getCarrinho()
		cliente = pagamento.getCliente()
		sql = "INSERT INTO PAGAMENTO(endereco_id, cliente_id, estado_id, total)VALUES(%s,%s, %s, %s) RETURNING id;"
		id_pagamento = pagamento.getEstado().getId()
		self.__cur.execute(sql, (cliente.getEndereco().getId(), cliente.getId(),id_pagamento, carrinho.getTotal()))
		idPagamento = self.__cur.fetchone()[0]
		self.__con.commit()
		for produto in carrinho.getProdutos():
			sql = "INSERT INTO pagamentoproduto(pagamento_id,produto_id,quantidade)VALUES(%s,%s,%s);"
			self.__cur.execute(sql, (idPagamento, produto.getId(), produto.getQuantidade()))
			self.__con.commit()
	def carrinho_de_compras(self, pagamento_id):
		carrinho = CarrinhoDeCompras()
		sql = "SELECT * FROM PAGAMENTOPRODUTO WHERE pagamento_id = %s"
		self.__cur.execute(sql, str(pagamento_id))
		rec = self.__cur.fetchall()
		produtos = []
		for r in rec:	
			produto = self.getProduto(r[2])
			produto.setQuantidade(int(r[3]))
			produtos.append(produto)
		carrinho.setProdutos(produtos)
		return carrinho 
	def getPagamentos(self):
		lista = []
		sql = "SELECT * FROM PAGAMENTO order by id"
		self.__cur.execute(sql)
		rec = self.__cur.fetchall()
		for r in rec:
			pagamento = Pagamento(r[0])
			cliente = self.get_cliente_por_id(r[2])
			endereco = self.pegar_endereco_por_id_cliente(r[2])
			cliente.setEndereco(endereco)
			# Pegando todos os produtos nessa compra
			carrinho = self.carrinho_de_compras(pagamento.getId())
			carrinho.setTotal(r[4])
			pagamento.setEstado(self.getEstadoPorId(r[3]))
			pagamento.setCarrinho(carrinho)
			pagamento.setCliente(cliente)
			lista.append(pagamento)
		return lista
	def getPagamentosPorCliente(self, idCliente):
		lista = []
		sql = "SELECT * FROM PAGAMENTO WHERE cliente_id = %s"
		self.__cur.execute(sql, str(idCliente))
		rec = self.__cur.fetchall()
		for r in rec:
			pagamento = Pagamento(r[0])
			cliente = self.get_cliente_por_id(r[2])
			endereco = self.pegar_endereco_por_id_cliente(r[2])
			cliente.setEndereco(endereco)
			# Pegando todos os produtos nessa compra
			carrinho = self.carrinho_de_compras(pagamento.getId())
			carrinho.setTotal(r[4])
			pagamento.setCarrinho(carrinho)
			pagamento.setCliente(cliente)
			pagamento.setEstado(self.getEstadoPorId(r[3]))
			lista.append(pagamento)
		return lista
	def trocar_estado(self, pagamento, estado):
		sql = "UPDATE pagamento SET \"estado_id\" = %s WHERE id = %s"
		self.__cur.execute(sql, (str(estado), str(pagamento)))
		self.__con.commit()