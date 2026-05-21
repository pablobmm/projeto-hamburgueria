from apps.extensions import db_serv
from datetime import datetime

class Pedido(db_serv.Model):
    __tablename__ = "pedidos"

    id = db_serv.Column(db_serv.Integer, primary_key=True)
    usuario_id = db_serv.Column(db_serv.Integer, db_serv.ForeignKey('usuarios.id'), nullable=False)
    valor_total = db_serv.Column(db_serv.Float, nullable=False)
    data_pedido = db_serv.Column(db_serv.DateTime, default=datetime.utcnow)
    status = db_serv.Column(db_serv.String(20), default="pendente") 
    mp_payment_id = db_serv.Column(db_serv.String(100), nullable=True) 

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "valor_total": self.valor_total,
            "data_pedido": self.data_pedido.strftime("%d/%m/%Y %H:%M:%S"),
            "status": self.status
        }