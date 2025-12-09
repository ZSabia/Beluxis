from decimal import Decimal
from datetime import datetime
from . import db
from sqlalchemy import Numeric
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#class User(db.Model):
#    __tablename__ = 'user'
#    id = db.Column(db.Integer, primary_key=True)

class Cliente(db.Model, UserMixin):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    avatar = db.Column(db.String(200), default='avatar1.jpg')
    is_admin = db.Column(db.Boolean, default=False)
    relacionados_pedidos = db.relationship('Pedido', back_populates='cliente')

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200), default='default.jpg')
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    preco = db.Column(Numeric(10, 2), nullable=False)  # use Decimal ao manipular
    estoque = db.Column(db.Integer, nullable=False)

class Servico(db.Model):
    __tablename__ = 'servico'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    preco = db.Column(Numeric(10, 2), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)  # duração em minutos
    relacionados_agendamentos = db.relationship('Agendamento', back_populates='servico')

class Agendamento(db.Model):
    __tablename__ = 'agendamento'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pendente', nullable=False)
    cliente = db.relationship('Cliente', backref='agendamentos')
    servico = db.relationship('Servico', back_populates='relacionados_agendamentos')

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, default=datetime.now, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(20), default='produto', nullable=False)  # 'produto' ou 'servico'
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=True)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=True)
    cliente = db.relationship('Cliente', back_populates='relacionados_pedidos')
    produto = db.relationship('Produto', backref='pedidos')
    servico = db.relationship('Servico', backref='pedidos')
