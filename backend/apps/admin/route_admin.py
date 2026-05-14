from flask import Blueprint, jsonify, request
from apps.lanche.model_lanche import Lanche, listarLanche, deletarLanche
from apps.erp.models import ItemEstoque, Pedido
from apps.extensions import db_serv
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

# --- Rotas de Produtos ---
@admin_bp.route('/api/admin/stats', methods=['GET'])
@admin_required
def get_stats():
    return jsonify({
        "faturamento": 1500.50,
        "colaboradores": 8,
        "top_lanches": [{"nome": "Double Bacon", "vendas": 45}]
    })
    
@admin_bp.route('/api/admin/produtos', methods=['GET'])
def listar_produtos_admin():
    try:
        lanches = listarLanche()
        return jsonify(lanches), 200
    except Exception as e:
        print(f"ERRO NO BACKEND: {e}")
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/api/admin/produtos', methods=['POST'])
def criar_produto():
    try:
        dados = request.get_json()
        novo_lanche = Lanche(
            nome=dados['nome'],
            descricao=dados['descricao'],
            preco=dados['preco'],
            imagem=dados.get('imagem', ''),
            categoria=dados.get('categoria', 'Burgers')
        )
        db_serv.session.add(novo_lanche)
        db_serv.session.commit()
        return jsonify({"mensagem": "Produto criado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
        
@admin_bp.route('/api/admin/produtos/<int:id>', methods=['PUT'])
def editar_produto(id):
    try:
        dados = request.get_json()
        lanche = Lanche.query.get(id)
        if not lanche:
            return jsonify({"erro": "Produto não encontrado"}), 404
        
        lanche.nome = dados.get('nome', lanche.nome)
        lanche.descricao = dados.get('descricao', lanche.descricao)
        lanche.preco = dados.get('preco', lanche.preco)
        lanche.imagem = dados.get('imagem', lanche.imagem)
        lanche.categoria = dados.get('categoria', lanche.categoria)
        
        db_serv.session.commit()
        return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/api/admin/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    try:
        resposta, status = deletarLanche(id)
        return jsonify(resposta), status
    except Exception as e:
        return jsonify({"Erro": str(e)}), 500

# --- Rotas de Estoque (Mini ERP) ---
@admin_bp.route('/api/admin/estoque', methods=['GET'])
def listar_estoque():
    try:
        itens = ItemEstoque.query.all()
        return jsonify([item.to_dict() for item in itens]), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/api/admin/estoque', methods=['POST'])
def cadastrar_item_estoque():
    try:
        dados = request.get_json()
        novo_item = ItemEstoque(
            nome_item=dados['nome_item'],
            quantidade=dados['quantidade'],
            unidade_medida=dados['unidade_medida']
        )
        db_serv.session.add(novo_item)
        db_serv.session.commit()
        return jsonify(novo_item.to_dict()), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/api/admin/estoque/<int:id>', methods=['PUT'])
def atualizar_estoque(id):
    try:
        dados = request.get_json()
        item = ItemEstoque.query.get(id)
        if not item:
            return jsonify({"erro": "Item não encontrado"}), 404
        
        item.quantidade = dados.get('quantidade', item.quantidade)
        db_serv.session.commit()
        return jsonify(item.to_dict()), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/api/admin/estoque/<int:id>', methods=['DELETE'])
def remover_item_estoque(id):
    try:
        item = ItemEstoque.query.get(id)
        if not item:
            return jsonify({"erro": "Item não encontrado"}), 404
        
        db_serv.session.delete(item)
        db_serv.session.commit()
        return jsonify({"mensagem": "Item removido com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# --- Rotas de Pedidos (Mini ERP) ---
@admin_bp.route('/api/admin/pedidos', methods=['GET'])
def listar_pedidos_admin():
    try:
        pedidos = Pedido.query.all()
        return jsonify([pedido.to_dict() for pedido in pedidos]), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
