import os
import requests
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
        total = sum(item['preco'] * item['qtd'] for item in itens)
        novo_pedido = Pedido(usuario_id=usuario_id, valor_total=total, status="pendente")
        
        db_serv.session.add(novo_pedido)
        db_serv.session.flush()

        api_key = os.getenv("ASAAS_API_KEY")
        url = "https://sandbox.asaas.com/api/v3/payments"
        
        headers = {
            "access_token": api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "customer": "cus_000006326120", 
            "billingType": "PIX",
            "value": total,
            "dueDate": "2026-12-31",
            "externalReference": str(novo_pedido.id)
        }

        response = requests.post(url, json=payload, headers=headers)
        asaas_res = response.json()

        if response.status_code != 200:
             return jsonify({"erro": "Erro no Asaas", "detalhes": asaas_res}), 400

        for item in itens:
            novo_item = ItemPedido(
                pedido_id=novo_pedido.id,
                lanche_id=item['lanche_id'],
                quantidade=item['qtd'],
                preco_unitario=item['preco']
            )
            db_serv.session.add(novo_item)

        db_serv.session.commit()

        return jsonify({
            "mensagem": "Pedido criado e PIX gerado!",
            "pedido_id": novo_pedido.id,
            "link_pagamento": asaas_res.get("invoiceUrl")
        }), 201

    except Exception as e:
        db_serv.session.rollback()
        return jsonify({"erro": str(e)}), 500