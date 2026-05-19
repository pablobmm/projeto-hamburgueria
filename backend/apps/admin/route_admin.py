import os
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from apps.lanche.model_lanche import Lanche, listarLanche, criarLanche, deletarLanche
from apps.extensions import db_serv

admin_bp = Blueprint('admin', __name__)

destinoPasta = os.path.join('frontend', 'assets', 'burgers')
extensoes = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensoes


@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    try:
        return jsonify({
            "faturamento": 1500.50,
            "colaboradores": 8,
            "top_lanches": [{"nome": "Double Bacon", "vendas": 45}]
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/produtos', methods=['GET'])
def listar_produtos_admin():
    try:
        lanches = listarLanche()
        return jsonify(lanches), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/produtos/<int:id>', methods=['GET'])
def obter_produto_individual(id):
    try:
        db_serv.session.expire_all()
        lanche = db_serv.session.get(Lanche, id)
        if not lanche:
            return jsonify({"erro": "Lanche não encontrado"}), 404
        return jsonify(lanche.to_dict()), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/produtos', methods=['POST'])
def criar_produto():
    try:
        nome = request.form.get('nome')
        descricao = request.form.get('descricao', '')
        preco = request.form.get('preco')
        categoria = request.form.get('categoria')
        
        foto = request.files.get('imagem')
        nome_imagem = "default_burger.png"

        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            if not os.path.exists(destinoPasta):
                os.makedirs(destinoPasta)
            foto.save(os.path.join(destinoPasta, filename))
            nome_imagem = filename

        id_categoria = int(categoria) if (categoria and str(categoria).isdigit()) else 1

        novo_lanche = Lanche(
            nome=nome,
            preco=float(preco) if preco else 0.0,
            descricao=descricao,
            imagem=nome_imagem,
            categoria_id=id_categoria
        )

        resposta, status = criarLanche(novo_lanche)
        return jsonify(resposta), status
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/produtos/<int:id>', methods=['PUT'])
def editar_produto(id):
    try:
        lanche = db_serv.session.get(Lanche, id)
        if not lanche:
            return jsonify({"erro": "Lanche não encontrado"}), 404

        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')
        categoria = request.form.get('categoria')

        if preco and isinstance(preco, str):
            preco = preco.replace(',', '.')

        imagem_antiga = lanche.imagem

        if nome: lanche.nome = nome
        if descricao is not None: lanche.descricao = descricao
        if preco: lanche.preco = float(preco)
        if categoria and str(categoria).isdigit():
            lanche.categoria_id = int(categoria)

        foto = request.files.get('imagem')
        if foto and allowed_file(foto.filename):
            if imagem_antiga and imagem_antiga not in ["burger1.png", "default_burger.png", ""]:
                restantes = db_serv.session.query(Lanche).filter(Lanche.imagem == imagem_antiga).count()
                if restantes <= 1:
                    caminho_antigo = os.path.join(destinoPasta, imagem_antiga)
                    if os.path.exists(caminho_antigo):
                        os.remove(caminho_antigo)

            filename = secure_filename(foto.filename)
            foto.save(os.path.join(destinoPasta, filename))
            lanche.imagem = filename 

        db_serv.session.commit()
        db_serv.session.expire_all()
        return jsonify({"mensagem": "Lanche atualizado com sucesso!"}), 200
    except Exception as e:
        db_serv.session.rollback()
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    try:
        resposta, status = deletarLanche(id)
        return jsonify(resposta), status
    except Exception as e:
        return jsonify({"erro": str(e)}), 500