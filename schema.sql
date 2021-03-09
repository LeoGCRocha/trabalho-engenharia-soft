create database browrrashoes;
create table cliente(
	id serial primary key,
	nome varchar(50) not null,
	senha text not null,
	email varchar(100) not null,
    cpf varchar(11) unique not null
);
create table produto(
	id serial primary key,
	nome varchar(50) not null,
	descricao varchar(200),
	preco numeric(15,2) not null,
	link_imagem text not null
);
create table endereco(
	id serial primary key,
	endereco varchar(100) not null,
	cep varchar(11) not null,
	cliente_id integer REFERENCES cliente (id) ON DELETE CASCADE
);