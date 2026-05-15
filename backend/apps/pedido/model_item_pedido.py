from apps.extensions import db_serv

class ItemPedido(db_serv.Model):
    __tablename__ = "itens_pedido"

    id = db_serv.Column(db_serv.Integer, primary_key=True)
    pedido_id = db_serv.Column(db_serv.Integer, db_serv.ForeignKey('pedidos.id'), nullable=False)
    lanche_id = db_serv.Column(db_serv.Integer, db_serv.ForeignKey('lanches.id'), nullable=False)
    quantidade = db_serv.Column(db_serv.Integer, nullable=False, default=1)
    preco_unitario = db_serv.Column(db_serv.Float, nullable=False) 

    def to_dict(self):
        return {
            "lanche_id": self.lanche_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario
        }