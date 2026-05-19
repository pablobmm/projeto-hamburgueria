import os
from apps.extensions import db_serv
from apps.categoria.model_categoria import Categoria

class Lanche (db_serv.Model):
    __tablename__ = "lanches"
    __table_args__ = {'extend_existing': True}

    id = db_serv.Column(db_serv.Integer, primary_key=True)
    nome = db_serv.Column(db_serv.String(60), nullable=False)
    preco = db_serv.Column(db_serv.Float, nullable=False)
    descricao = db_serv.Column(db_serv.String(450), nullable=False)
    categoria_id = db_serv.Column(db_serv.ForeignKey('categorias.id'), nullable=False)
    imagem = db_serv.Column(db_serv.String(255))
    
    def __init__(self, nome=None, preco=None, descricao=None, imagem=None, categoria_id=1, id=None, **kwargs):
        if id: self.id = id
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.imagem = imagem
        self.categoria_id = categoria_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "descricao": self.descricao,
            "categoria": self.categoria_id, 
            "imagem": self.imagem
        }

    
class LancheJaExiste(Exception):
    def __init__(self, msg="Erro, já existe um lanche com esse id!"):
        self.msg = msg
        super().__init__(self.msg)

class LancheNaoExiste(Exception):
    def __init__(self, msg="Erro, o lanche não existe!"):
        self.msg = msg
        super().__init__(self.msg)

class CadastroDeLancheFalhado(Exception):
    def __init__(self, msg="Erro ao processar o cadastro do lanche!"):
        self.msg = msg
        super().__init__(msg)


def criarLanche(nv_dict):
    try:
        db_serv.session.add(nv_dict)
        db_serv.session.commit()
        return {"Descrição": "Lanche criado com êxito!"}, 200
    except Exception as e:
        db_serv.session.rollback()
        return {"erro": str(e)}, 500

def listarLanche():
    db_serv.session.expire_all()    
    lanches = Lanche.query.all()
    return [lanche.to_dict() for lanche in lanches]

def lancheExiste(id):
    lanche = db_serv.session.get(Lanche, id)
    return lanche is not None

def deletarLanche(id_lanche):
    try:
        destinoPasta = os.path.join('frontend', 'assets', 'burgers')

        lanche = db_serv.session.get(Lanche, id_lanche)
        
        if not lanche:
            return {"Mensagem": "Lanche não encontrado no banco!"}, 404
            
        nome_imagem = lanche.imagem

        if nome_imagem and nome_imagem not in ["burger1.png", "default_burger.png", ""]:
            restantes = db_serv.session.query(Lanche).filter(Lanche.imagem == nome_imagem).count()
            
            deve_apagar_arquivo = (restantes <= 1)
        else:
            deve_apagar_arquivo = False

        db_serv.session.delete(lanche)
        db_serv.session.commit()

        if deve_apagar_arquivo:
            caminho_arquivo = os.path.join(destinoPasta, nome_imagem)
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
                print(f"Arquivo {nome_imagem} removido do disco porque era usado apenas pelo lanche deletado.")
        else:
            if nome_imagem and nome_imagem not in ["burger1.png", "default_burger.png", ""]:
                print(f"Arquivo {nome_imagem} MANTIDO no disco. Outro lanche ainda está utilizando ele.")

        db_serv.session.expire_all()
        return {"Mensagem": "Lanche deletado com sucesso!"}, 200

    except Exception as e:
        db_serv.session.rollback() 
        db_serv.session.expire_all()
        print(f"Erro ao deletar lanche via ORM: {e}")
        return {"Erro": str(e)}, 500