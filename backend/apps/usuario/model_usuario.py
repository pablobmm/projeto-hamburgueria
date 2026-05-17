from apps.app import db_serv
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(db_serv.Model):
    __tablename__ = 'usuarios' 
    id = db_serv.Column(db_serv.Integer, primary_key=True)
    nome = db_serv.Column(db_serv.String(100), nullable=False)
    email = db_serv.Column(db_serv.String(100), unique=True, nullable=False)
    telefone = db_serv.Column(db_serv.String(20), nullable=True)
    endereco = db_serv.Column(db_serv.String(200), nullable=False)
    numero = db_serv.Column(db_serv.String(10), nullable=False)
    bairro = db_serv.Column(db_serv.String(100), nullable=False)
    cep = db_serv.Column(db_serv.String(9), nullable=True)
    senha_hash = db_serv.Column(db_serv.String(256), nullable=False) 
    otp_secret = db_serv.Column(db_serv.Integer, nullable=True) 
    is_active = db_serv.Column(db_serv.Boolean, default= False, nullable=False) 


    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'numero': self.numero,
            'bairro': self.bairro,
            'cep':self.cep,
            'otp_secret': self.otp_secret,
            'is_active': self.is_active
        }

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)