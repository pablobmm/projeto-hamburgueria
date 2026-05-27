import random, string
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from apps.extensions import db_serv
from apps.usuario.model_usuario import Usuario 
from sqlalchemy import func

bd_usuario = Blueprint('usuario', __name__)

@bd_usuario.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    dados = request.get_json()
    email_cliente = dados.get('email')
    nome_cliente = dados.get('nome')
    senha_cliente = dados.get('senha')

    token_ativacao = ''.join(random.choices(string.digits, k=6))

    novo_usuario = Usuario(
        nome=nome_cliente,
        email=email_cliente,
        telefone=dados.get('telefone'),
        endereco=dados.get('endereco'),
        numero=dados.get('numero'),
        bairro=dados.get('bairro'),
        cep=dados.get('cep'),
        senha_hash=generate_password_hash(senha_cliente),
        otp_secret=token_ativacao,
        is_active=False
    )

    try:
        db_serv.session.add(novo_usuario)
        db_serv.session.commit()
        print(f"Usuário {nome_cliente} salvo com sucesso no banco!")

        return jsonify({
            "message": "Usuário cadastrado com sucesso!",
            "token": token_ativacao,
            "nome": nome_cliente,
            "email": email_cliente
        }), 201

    except Exception as e:
        db_serv.session.rollback()
        print(f"Erro no banco: {str(e)}")
        return jsonify({"erro": "Este e-mail já está cadastrado ou ocorreu um erro no servidor."}), 500
    
@bd_usuario.route('/recuperar-senha', methods=['POST'])
def recuperar_senha():
    dados = request.get_json()
    email_usuario = dados.get('email')

    usuario = Usuario.query.filter(func.lower(Usuario.email) == func.lower(email_usuario)).first()
    
    if not usuario:
        return jsonify({"message": "Usuário não encontrado."}), 404

    codigo_recuperacao = ''.join(random.choices(string.digits, k=6))

    try:
        usuario.otp_secret = codigo_recuperacao
        db_serv.session.commit()

        return jsonify({
            "status": "success",
            "message": "Código de recuperação gerado com sucesso!",
            "token": codigo_recuperacao,
            "nome": usuario.nome,
            "email": email_usuario
        }), 200

    except Exception as e:
        db_serv.session.rollback()
        return jsonify({
            "message": "Erro ao processar recuperação de senha.",
            "error": str(e)
        }), 500

@bd_usuario.route('/reenviar-codigo', methods=['POST'])
def reenviar_codigo():
    data = request.get_json()
    email = data.get('email')
    
    usuario = Usuario.query.filter(func.lower(Usuario.email) == func.lower(email)).first()
    
    if usuario:
        novo_codigo = str(random.randint(100000, 999999))
        usuario.otp_secret = novo_codigo
        
        try:
            db_serv.session.add(usuario)
            db_serv.session.commit()

            return jsonify({
                "mensagem": "Novo código gerado com sucesso!",
                "token": novo_codigo,
                "nome": usuario.nome,
                "email": email
            }), 200
        except Exception as e:
            db_serv.session.rollback()
            print(f"Erro ao salvar reenvio: {e}")
            return jsonify({"erro": "Falha ao gerar novo código no servidor"}), 500
            
    return jsonify({"erro": "Usuário não encontrado."}), 404


@bd_usuario.route('/verificar', methods=['POST'])
def verificar_codigo():
    data = request.get_json()
    email = data.get('email')
    codigo_recebido = data.get('codigo')

    if not email or not codigo_recebido:
        return jsonify({"erro": "Email e código são obrigatórios"}), 400

    usuario = Usuario.query.filter(func.lower(Usuario.email) == func.lower(email)).populate_existing().first()

    if usuario and usuario.otp_secret is not None:
        if str(usuario.otp_secret) == str(codigo_recebido):
            try:
                usuario.is_active = True
                usuario.otp_secret = None 
                
                db_serv.session.add(usuario)
                db_serv.session.commit()
                
                return jsonify({"mensagem": "Conta ativada com sucesso!"}), 200
            except Exception as e:
                db_serv.session.rollback()
                print(f"ERRO CRÍTICO NO COMMIT: {e}")
                return jsonify({"erro": f"Erro interno ao salvar: {str(e)}"}), 500
        else:
            return jsonify({"erro": "Código de verificação inválido."}), 400
    
    return jsonify({"erro": "Usuário não encontrado ou já ativado."}), 404

@bd_usuario.route('/atualizar/<int:id>', methods=['PUT'])
def atualizar_perfil(id):
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    dados = request.get_json()
    
    usuario.nome = dados.get('nome', usuario.nome)
    usuario.telefone = dados.get('telefone', usuario.telefone)
    usuario.endereco = dados.get('endereco', usuario.endereco)
    
    novo_email = dados.get('email')
    if novo_email and novo_email != usuario.email:
        email_existe = Usuario.query.filter_by(email=novo_email).first()
        if email_existe:
            return jsonify({"erro": "Este e-mail já está em uso por outra conta."}), 400
        usuario.email = novo_email

    try:
        db_serv.session.commit()
        return jsonify({
            "mensagem": "Dados updated com sucesso!",
            "usuario": usuario.to_dict()
        }), 200
    except Exception as e:
        db_serv.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar: {str(e)}"}), 500