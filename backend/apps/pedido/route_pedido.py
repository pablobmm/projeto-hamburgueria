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
        return jsonify({"erro": "Dados insuficientes para processar o checkout. Certifique-se de estar logado."}), 400
    
    try:
        mp_token = os.environ.get("MERCADOPAGO_ACCESS_TOKEN")
        if not mp_token:
            print("ERRO CRÍTICO: MERCADOPAGO_ACCESS_TOKEN nao foi encontrado no Render!")
            return jsonify({"erro": "Configuração do meio de pagamento ausente no servidor do Render."}), 500

        sdk = mercadopago.SDK(mp_token)

        total = sum(float(item['preco']) * int(item['qtd']) for item in itens)
        
        novo_pedido = Pedido(usuario_id=int(usuario_id), valor_total=total, status="pendente")
        db_serv.session.add(novo_pedido)
        db_serv.session.flush() 

        preference_data = {
            "items": [
                {
                    "title": f"Pedido Code Burger #{novo_pedido.id}",
                    "quantity": 1,
                    "unit_price": float(total),
                    "currency_id": "BRL"
                }
            ],
            "payer": {
                "email": payer_email,
                "name": payer_name
            },
            "back_urls": {
                "success": "https://code-burger-kappa.vercel.app/pages/index.html",
                "failure": "https://code-burger-kappa.vercel.app/pages/carrinho.html",
                "pending": "https://code-burger-kappa.vercel.app/pages/carrinho.html"
            },
            "external_reference": str(novo_pedido.id),
            "notification_url": "https://code-burger-api.onrender.com/pedido/webhook"
        }

        preference_response = sdk.preference().create(preference_data)
        mp_res = preference_response.get("response", {})

        print(f"RETORNO DO MERCADO PAGO: {mp_res}")

        if "id" not in mp_res:
            db_serv.session.rollback()
            return jsonify({"erro": "O Mercado Pago recusou as credenciais enviadas.", "detalhes": mp_res}), 400

        novo_pedido.mp_payment_id = str(mp_res.get("id")) 

        for item in itens:
            novo_item = ItemPedido(
                pedido_id=novo_pedido.id,
                lanche_id=int(item['lanche_id']),
                quantidade=int(item['qtd']),
                preco_unitario=float(item['preco'])
            )
            db_serv.session.add(novo_item)

        db_serv.session.commit()

        link_pagamento = mp_res.get("sandbox_init_point") or mp_res.get("init_point")

        return jsonify({
            "mensagem": "Pedido e Checkout criados com sucesso via Mercado Pago!",
            "pedido_id": novo_pedido.id,
            "link_pagamento": link_pagamento
        }), 201

    except Exception as e:
        db_serv.session.rollback()
        print(f"EXCEÇÃO CRÍTICA NO CHECKOUT: {str(e)}")
        return jsonify({"erro": "Erro interno no servidor ao processar pagamento.", "detalhes": str(e)}), 500
    
@pedido_bp.route('/webhook', methods=['POST'])
def webhook():
    id_pagamento = request.args.get('data.id') or request.args.get('id')
    type_notificacao = request.args.get('type') or request.get_json().get('type')

    if type_notificacao == 'payment' or request.args.get('topic') == 'payment':
        if not id_pagamento:
            dados_corpo = request.get_json() or {}
            if 'data' in dados_corpo:
                id_pagamento = dados_corpo['data'].get('id')

        if id_pagamento:
            try:
                mp_token = os.environ.get("MERCADOPAGO_ACCESS_TOKEN")
                sdk = mercadopago.SDK(mp_token)
                
                payment_info = sdk.payment().get(id_pagamento)
                payment_data = payment_info["response"]

                pedido_id_sistema = payment_data.get("external_reference")
                status_pagamento = payment_data.get("status") 

                if pedido_id_sistema:
                    pedido = Pedido.query.get(int(pedido_id_sistema))
                    
                    if pedido:
                        if status_pagamento == "approved":
                            pedido.status = "pago"
                        else:
                            pedido.status = status_pagamento 
                        
                        pedido.mp_payment_id = str(id_pagamento)
                        db_serv.session.commit()
                        print(f"Pedido #{pedido_id_sistema} atualizado via Webhook para {status_pagamento}!")
                        
            except Exception as error_webhook:
                db_serv.session.rollback()
                print(f"Erro ao processar webhook do Mercado Pago: {error_webhook}")
                return jsonify({"erro": "Erro interno ao processar notificacao", "detalhes": str(error_webhook)}), 500

    return jsonify({"status": "recebido"}), 200