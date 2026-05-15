from flask import Blueprint, request, jsonify
from apps.extensions import db_serv
from apps.pedido.model_pedido import Pedido
from apps.pedido.model_item_pedido import ItemPedido

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/checkout', methods=['POST'])
def checkout():
    dados = request.get_json()
    usuario_id = dados.get('usuario_id')
    itens = dados.get('itens') 
    
    try:
        novo_pedido = Pedido(
            usuario_id=usuario_id,
            valor_total=sum(item['preco'] * item['qtd'] for item in itens),
            status="pendente"
        )
        db_serv.session.add(novo_pedido)
        db_serv.session.flush() 

        for item in itens:
            novo_item = ItemPedido(
                pedido_id=novo_pedido.id,
                lanche_id=item['lanche_id'],
                quantidade=item['qtd'],
                preco_unitario=item['preco']
            )
            db_serv.session.add(novo_item)

        db_serv.session.commit()
        return jsonify({"mensagem": "Pedido realizado!", "pedido_id": novo_pedido.id}), 201

    except Exception as e:
        db_serv.session.rollback()
        return jsonify({"erro": str(e)}), 500