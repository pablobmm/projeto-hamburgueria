import os
import mercadopago
from flask import Blueprint, request, jsonify
from apps.extensions import db_serv
from apps.pedido.model_pedido import Pedido
from apps.pedido.model_item_pedido import ItemPedido

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/checkout', methods=['POST'])
def checkout():
    dados = request.get_json() or {}
    usuario_id = dados.get('usuario_id')
    itens = dados.get('itens', [])
    
    payer_email = dados.get('email', 'teste@teste.com')
    payer_name = dados.get('nome', 'Cliente')

    if not usuario_id or not itens:
        return jsonify({"erro": "Dados insuficientes para processar o checkout."}), 400
    
    try:
        mp_token = os.environ.get("MERCADOPAGO_ACCESS_TOKEN")
        if not mp_token:
            return jsonify({"erro": "Configuração do meio de pagamento ausente no servidor."}), 500

        sdk = mercadopago.SDK(mp_token)

        total = sum(item['preco'] * item['qtd'] for item in itens)
        
        novo_pedido = Pedido(usuario_id=usuario_id, valor_total=total, status="pendente")
        db_serv.session.add(novo_pedido)
        db_serv.session.flush()

        payment_data = {
            "transaction_amount": float(total),
            "description": f"Pedido Code Burger #{novo_pedido.id}",
            "payment_method_id": "pix",
            "external_reference": str(novo_pedido.id),
            "payer": {
                "email": payer_email, 
                "first_name": payer_name
            }
        }

        payment_response = sdk.payment().create(payment_data)
        mp_res = payment_response["response"]

        if "id" not in mp_res:
            db_serv.session.rollback()
            return jsonify({"erro": "Falha ao gerar pagamento no Mercado Pago", "detalhes": mp_res}), 400

        novo_pedido.mp_payment_id = str(mp_res.get("id")) 

        for item in itens:
            novo_item = ItemPedido(
                pedido_id=novo_pedido.id,
                lanche_id=item['lanche_id'],
                quantidade=item['qtd'],
                preco_unitario=item['preco']
            )
            db_serv.session.add(novo_item)

        db_serv.session.commit()

        transaction_data = mp_res.get("point_of_interaction", {}).get("transaction_data", {})
        link_pix = transaction_data.get("ticket_url")

        return jsonify({
            "mensagem": "Pedido e PIX criados com sucesso via Mercado Pago!",
            "pedido_id": novo_pedido.id,
            "link_pagamento": link_pix
        }), 201

    except Exception as e:
        db_serv.session.rollback()
        print(f"ERRO NO CHECKOUT MERCADO PAGO: {e}")
        return jsonify({"erro": "Erro interno ao processar o checkout."}), 500