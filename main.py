# coding: utf-8
from flask import Flask, render_template, url_for, redirect, session, request
import hashlib
from dominio.cliente import Cliente
from servicostecnicos.conexao import Conexao
from dominio.produto import Produto
import sys
app = Flask(__name__, template_folder='templates')
app.secret_key = "sLqX6wtpQn"
c = Conexao()
import importlib
importlib.reload(sys)
# SOLUÇÃO PARA ERRO DE ROTAS
# ROTAS
@app.route('/')
def main_page():
  if 'login' not in session:
      return render_template('index.html')
  else:
    if session['login'] == "admin@admin":
      return redirect(url_for("admin"))
    else:
      prod = c.getProdutos()
      clienteAtual = c.get_cliente_por_id(session['login'])
      isDefinido = clienteAtual.getEndereco() == None
      return render_template('home.html', u = clienteAtual, produtos = prod, semEndereco = isDefinido)
# METODO PARA EFETUAR LOGIN
# DESENVOLVER PAGINA INICIAL PARA ADMIN
@app.route('/logar', methods=['POST'])
def logar():
  senha = request.form.get('senha')
  email = request.form['email']
  if email == "admin@admin":
    if senha == "admin":
      session['login'] = "admin@admin"
      return redirect(url_for("admin"))
  else:
    clientes = c.clientes()
    for user in clientes:
      if user.getEmail() == email:
        if senha == user.getSenha():
          session['login'] = user.getId()
          session['email'] = user.getEmail()
          session['carrinho_de_compras'] = []
  return redirect(url_for('main_page'))
# ADMIN PAGE
@app.route("/admin")
def admin():
  return render_template("admin.html")
# ENDEREÇO PARA PAGINA DE REGISTRO
@app.route("/registro")
def registro():
  if 'login' in session:
    redirect(url_for('main_page')) # USUARIO JA ESTA LOGADO E DEVE SER REDIRECIONADO
  else:
    return render_template("registro.html")
# PAGINA PARA EDITAR ENDEREÇO 
@app.route("/editar_endereco")
def endereco():
  return render_template("editar_endereco.html")
# METODO PARA REALIZAÇÃO DO REGISTRO
@app.route("/registrar", methods= ['POST'])
def registrar():
  if request.method == 'POST':
    nome  = request.form['nome']
    email = request.form['email']
    cpf = request.form['cpf']
    m = hashlib.md5()
    senha = request.form['senha'] # PARA SENHA NÃO FICAR SENDO VISIVEL NO BANCO DE DADOS
    cliente = Cliente(0,cpf, nome,email,senha) # ID FICA PADRÃO 0 POIS O BANCO DE DADOS IRA DEFINIR
    c.cadastrar(cliente)
  return redirect(url_for('main_page'))
# METODO PARA AJUSTAR ENDERECO 
@app.route("/metodo_editar_endereco", methods= ['POST'])
def metodo_editar_endereco():
  if request.method == 'POST':
    pass # CONTINUAR DAQUI
  return redirect(url_for('main_page'))
# LOGOUT
@app.route("/deslogar")
def deslogar():
  if 'login' in session:
    session.clear()
  return redirect(url_for('main_page')) 
# PAGINA LOGIN
@app.route("/home")
def home():
  notLogin()
  # PAGINA ONDE SÃO REALIZADA AS VENDAS DE PRODUTOS
  return render_template('home.html')
# NOT LOGIN REDIRECT
def notLogin():
  if 'login' not in session:
    redirect(url_for('main_page'))
# ERROR PAGE
@app.route("/error/<description>/<errorId>")
def error(description, errorId):
  return render_template("error.html", description = description, errorId = errorId)
# ERROR 404 NOT FOUND
@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html', description = "Página não encontrada!", errorId = "404"), 404
# ADMIN
@app.route('/admin_cliente')
def admin_cliente():
  admin = isAdmin()
  if admin:
    cli = c.clientes()
    return render_template("admin_cliente.html", clientes = cli)
  else:
    return redirect(url_for('error', description="Você não tem permissão!", errorId = "403"))
# DELETAR CLIENTE
@app.route('/deletar_cliente/<id>')
def deletar_cliente(id):  
  admin = isAdmin()
  if admin:
    c.deletar_cliente_por_id(id)
    return redirect(url_for('admin_cliente'))
  else:
    return redirect(url_for('error', description="Você não tem permissão!", errorId = "403"))
# EDITAR CLIENTE
@app.route("/editar_cliente/<id>")
def pagEditarCliente(id):
  admin = isAdmin()
  if admin:
    cliente = c.get_cliente_por_id(id)
    return render_template("editar_cliente.html", cli = cliente)
  else:
    return redirect(url_for('error', description="Você não tem permissão!", errorId = "403"))
@app.route("/editar_cliente_metodo", methods = ['POST'])
def editarCliente():
  nome = request.form['nome']
  cpf = request.form['cpf']
  email = request.form['email']
  cliente = c.get_cliente_por_id(request.form['idInput'])
  cliente.setNome(nome)
  cliente.setEmail(email)
  cliente.setCpf(cpf)
  c.editarCliente(cliente)
  return redirect(url_for('admin_cliente'))
# PAGINA ADMIN PRODUTO
@app.route("/admin_produto")
def admin_produto():
  admin = isAdmin()
  if admin:
    listaProdutos = c.getProdutos()
    return render_template("admin_produto.html", produtos = listaProdutos)
  else:
    return redirect(url_for('error', description="Você não tem permissão!", errorId = "403"))
@app.route("/registrar_produto", methods= ['POST'])
def registrar_produto():
  if request.method == 'POST':
    nome  = request.form['nome']
    descricao = request.form['descricao']
    preco = request.form['preco']
    linkImagem = request.form['imagem']
    produto = Produto(0, nome,descricao ,preco, linkImagem) # ID FICA PADRÃO 0 POIS O BANCO DE DADOS IRA DEFINIR
    c.cadastrar_produto(produto)
  return redirect(url_for('admin_produto'))
@app.route('/deletar_produto/<id>')
def deletar_produto(id):  
  admin = isAdmin()
  if admin:
    c.deletar_produto(id)
    return redirect(url_for('admin_produto'))
  else:
    return redirect(url_for('error', description="Você não tem permissão!", errorId = "403"))
@app.route("/editar_produto/<id>")
def editar_produto(id):
  admin = isAdmin()
  if admin:
    prod = c.getProduto(id)
    return render_template("editar_produto.html", produto = prod)
  else:
    return redirect(url_for('error', description="Você não tem permissão!", errorId = "403"))
@app.route("/editar_produto_metodo", methods = ["POST"])
def editar_produto_metodo():
  if request.method == "POST":
    prodId = request.form['id']
    nome  = request.form['nome']
    descricao = request.form['descricao']
    preco = request.form['preco']
    linkImagem = request.form['imagem']
    produto = Produto(prodId, nome,descricao ,preco, linkImagem)
    c.editar_produto(produto)
  return redirect(url_for('admin_produto'))
# ADICONAR AO CARRINHO DE COMPRAS
@app.route("/adicionar_carrinho/<id>")
def adicionar_carrinho(id):
  notLogin()
  lista = session['carrinho_de_compras']
  produtoEncontrado = False
  for a in range(0, len(lista)):
    codAtual = lista[a].split("#")
    if codAtual[0] == id:
      produtoEncontrado = True
      lista[a] = codAtual[0]+"#"+str(int(codAtual[1])+1)
  if not produtoEncontrado:
    lista.append(str(id)+"#1")
  session['carrinho_de_compras'] = lista
  return redirect(url_for('carrinho_de_compras')) # USUARIO JA ESTA LOGADO E DEVE SER REDIRECIONADO
@app.route("/carrinho_de_compras")
def carrinho_de_compras():
  notLogin()
  lista = session['carrinho_de_compras']
  prodList = []
  quant = []
  total = 0
  for a in range(0, len(lista)):
    codAtual = lista[a].split("#")
    prod = c.getProduto(codAtual[0])
    quant.append(str(codAtual[1]))
    total = total + (int(prod.getPreco()) * int(codAtual[1]))
    prod.setQuantidade(int(codAtual[1]))
    prodList.append(prod)
  return render_template("carrinho_de_compras.html", produtos = prodList, tot = total)
@app.route("/remover_carrinho/<id>")
def remover_carrinho(id):
  notLogin()
  lista = session['carrinho_de_compras']
  for a in range(0, len(lista)):
    codAtual = lista[a].split("#")
    if codAtual[0] == id:
      lista.remove(lista[a])
  session['carrinho_de_compras'] = lista
  return redirect(url_for('carrinho_de_compras'))
# IS ADMIN ?!
def isAdmin():
  if 'login' not in session:
    return False
  else:
    if session['login'] != "admin@admin":
      return False
  return True
def run():
    app.run(debug=True)
run()
