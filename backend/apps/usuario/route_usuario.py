import random, string
from flask import request, jsonify, Blueprint, current_app
from werkzeug.security import generate_password_hash
from flask_mail import Message
from apps.extensions import db_serv, mail 
from apps.usuario.model_usuario import Usuario 

bd_usuario = Blueprint('usuario', __name__)

@bd_usuario.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    dados = request.get_json()
    email_cliente = dados.get('email')
    nome_cliente = dados.get('nome')
    senha_cliente = dados.get('senha')

    # 1. Gerar o token de 6 dígitos
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
        # SALVA NO BANCO PRIMEIRO
        db_serv.session.add(novo_usuario)
        db_serv.session.commit()
        print(f"Usuário {nome_cliente} salvo com sucesso!")

        # TENTA ENVIAR O E-MAIL (Se falhar, não trava o cadastro)
        try:
            msg = Message(
                subject="Ative sua conta - Code Burger",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email_cliente],
                body=f"Olá {nome_cliente}!\n\nSeu código de ativação é: {token_ativacao}"
            )
            mail.send(msg)
            print("E-mail enviado com sucesso!")
        except Exception as e_mail:
            print(f"Erro ao enviar e-mail: {e_mail}")
            # Não retornamos erro aqui para o front não travar

        return jsonify({"message": "Usuário cadastrado! Verifique seu e-mail."}), 201

    except Exception as e:
        db_serv.session.rollback()
        print(f"Erro no banco: {str(e)}")
        return jsonify({"erro": "Este e-mail já está cadastrado ou ocorreu um erro no servidor."}), 500

@bd_usuario.route('/recuperar-senha', methods=['POST'])
def recuperar_senha():
    dados = request.get_json()
    email_usuario = dados.get('email')

    # Busca o usuário para salvar o código
    usuario = Usuario.query.filter_by(email=email_usuario).first()
    
    if not usuario:
        return jsonify({"message": "Usuário não encontrado."}), 404

    # Código aleatório de 6 dígitos
    codigo_recuperacao = ''.join(random.choices(string.digits, k=6))

    try:
        # Salva o código no banco na coluna otp_secret 
        usuario.otp_secret = codigo_recuperacao
        db_serv.session.commit()

        # Criar e enviar a mensagem
        msg = Message(
            subject="Recuperação de Senha - Code Burger",
            recipients=[email_usuario],
            body=f"Olá!\n\nRecebemos uma solicitação de recuperação de senha.\n"
                 f"Seu código de segurança é: {codigo_recuperacao}\n\n"
                 f"Se você não solicitou isso, ignore este e-mail."
        )
        mail.send(msg)
        
        return jsonify({
            "message": "Código de recuperação enviado com sucesso!",
            "status": "success"
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
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario:
        # Gera novo código de 6 dígitos
        novo_codigo = str(random.randint(100000, 999999))
        usuario.otp_secret = novo_codigo
        
        db_serv.session.add(usuario)
        db_serv.session.commit()

        try:
            msg = Message(
                subject="Novo código de ativação - Code Burger",
                recipients=[email],
                body=f"Seu novo código é: {novo_codigo}"
            )
            mail.send(msg)
            return jsonify({"mensagem": "Novo código enviado!"}), 200
        except Exception as e:
            print(f"Erro ao enviar reenvio: {e}")
            return jsonify({"erro": "Falha ao enviar e-mail"}), 500



@bd_usuario.route('/verificar', methods=['POST'])
def verificar_codigo():
    data = request.get_json()
    email = data.get('email')
    codigo_recebido = data.get('codigo')

    if not email or not codigo_recebido:
        return jsonify({"erro": "Email e código são obrigatórios"}), 400

    # .populate_existing() garante que pegou os dados do banco
    usuario = Usuario.query.filter_by(email=email).populate_existing().first()

    if usuario and usuario.otp_secret is not None:
        # Compara o código salvo no banco com o que o usuário digitou
        if str(usuario.otp_secret) == str(codigo_recebido):
            try:
                # Ativa a conta
                usuario.is_active = True
                usuario.otp_secret = None # Limpa o código para não ser usado de novo
                
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
            "mensagem": "Dados atualizados com sucesso!",
            "usuario": usuario.to_dict()
        }), 200
    except Exception as e:
        db_serv.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar: {str(e)}"}), 500