from beluxis import db
from datetime import datetime 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    pass

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    relacionados_pedidos = db.relationship('Pedido', backref='cliente', lazy=True)
    pass

class Produto(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200), default='default.jpg')
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    pass

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(50), nullable=False)
    pass