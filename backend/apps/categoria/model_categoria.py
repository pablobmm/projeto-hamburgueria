from apps.app import db_serv

class Categoria(db_serv.Model):
    __tablename__="categorias"

    id = db_serv.Column(db_serv.Integer, primary_key= True)
    nome = db_serv.Column(db_serv.String(60), nullable = False)
