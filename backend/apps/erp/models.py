from apps.extensions import db_serv
from datetime import datetime

# Tabela associativa para Itens do Pedido
itens_pedido = db_serv.Table('itens_pedido',
    db_serv.Column('pedido_id', db_serv.Integer, db_serv.ForeignKey('pedidos.id'), primary_key=True),
    db_serv.Column('lanche_id', db_serv.Integer, db_serv.ForeignKey('lanches.id'), primary_key=True),
    db_serv.Column('quantidade', db_serv.Integer, nullable=False, default=1)
)

class ItemEstoque(db_serv.Model):
    __tablename__ = 'estoque'
    id = db_serv.Column(db_serv.Integer, primary_key=True)
    nome_item = db_serv.Column(db_serv.String(100), nullable=False)
    quantidade = db_serv.Column(db_serv.Float, nullable=False, default=0.0)
    unidade_medida = db_serv.Column(db_serv.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome_item': self.nome_item,
            'quantidade': self.quantidade,
            'unidade_medida': self.unidade_medida
        }

class Pedido(db_serv.Model):
    __tablename__ = 'pedidos'
    id = db_serv.Column(db_serv.Integer, primary_key=True)
    usuario_id = db_serv.Column(db_serv.Integer, db_serv.ForeignKey('usuarios.id'), nullable=False)
    data_pedido = db_serv.Column(db_serv.DateTime, default=datetime.utcnow)
    status = db_serv.Column(db_serv.String(50), nullable=False, default='pendente')
    valor_total = db_serv.Column(db_serv.Float, nullable=False)

    # Relacionamentos
    cliente = db_serv.relationship('Usuario', backref=db_serv.backref('pedidos', lazy=True))
    itens = db_serv.relationship('Lanche', secondary=itens_pedido, lazy='subquery',
                                backref=db_serv.backref('pedidos', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'cliente_nome': self.cliente.nome if self.cliente else "Desconhecido",
            'data_pedido': self.data_pedido.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'valor_total': self.valor_total,
            'itens': [item.nome for item in self.itens]
        }
