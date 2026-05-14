import os
from apps.admin.route_admin import admin_bp
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from apps.extensions import db_serv, mail 
from flask_mail import Message
app = Flask(__name__)
CORS(app)

# CONFIGURAÇÕES DE E-MAIL DINÂMICAS
app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.environ.get("MAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = os.environ.get("MAIL_USE_TLS", "True") == "True"
app.config['MAIL_USE_SSL'] = os.environ.get("MAIL_USE_SSL", "False") == "True"
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME")

# CONFIGURAÇÃO DO BANCO DE DADOS
DB_USER = os.environ.get("MYSQL_USER_APP", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD_APP", "12345")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "hamburgueria")

if not os.environ.get("DB_HOST"):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hamburgueria.db"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# INICIALIZAÇÃO DAS EXTENSÕES 
db_serv.init_app(app)
mail.init_app(app)
swagger = Swagger(app)

# CONFIGURAÇÕES GERAIS
app.config['HOST'] = "0.0.0.0"
app.config['PORT'] = 5002
app.config['DEBUG'] = True

# REGISTRO DE BLUEPRINTS 
from apps.lanche.route_lanche import bd_Lanche
from apps.usuario.route_usuario import bd_usuario
from apps.login.route_login import bd_login

app.register_blueprint(bd_Lanche)
app.register_blueprint(bd_usuario, url_prefix='/usuario')
app.register_blueprint(bd_login)
app.register_blueprint(admin_bp, url_prefix='/admin')
if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])