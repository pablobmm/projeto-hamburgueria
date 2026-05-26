import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from apps.extensions import db_serv, mail 

app = Flask(__name__)

CORS(app)

IS_PRODUCTION = os.environ.get("RENDER", "False") == "true"

# CONFIGURAÇÕES DE E-MAIL DINÂMICAS
app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.environ.get("MAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = os.environ.get("MAIL_USE_TLS", "True") == "True"
app.config['MAIL_USE_SSL'] = os.environ.get("MAIL_USE_SSL", "False") == "True"
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME")

# CONFIGURAÇÃO DO BANCO DE DADOS 
DB_USER = os.environ.get("MYSQL_USER_APP") if IS_PRODUCTION else os.environ.get("MYSQL_USER_APP", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD_APP") if IS_PRODUCTION else os.environ.get("MYSQL_PASSWORD_APP", "12345")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# INICIALIZAÇÃO DAS EXTENSÕES 
db_serv.init_app(app)
swagger = Swagger(app)

# CONFIGURAÇÕES GERAIS 
app.config['HOST'] = "0.0.0.0"
app.config['PORT'] = 5002
app.config['DEBUG'] = False if IS_PRODUCTION else True

# REGISTRO DE BLUEPRINTS 
from apps.lanche.route_lanche import bd_Lanche
from apps.usuario.route_usuario import bd_usuario
from apps.login.route_login import bd_login
from apps.pedido.model_pedido import Pedido
from apps.pedido.model_item_pedido import ItemPedido
from apps.pedido.route_pedido import pedido_bp
from apps.admin.route_admin import admin_bp

app.register_blueprint(bd_Lanche, url_prefix='/api')
app.register_blueprint(bd_usuario, url_prefix='/usuario')
app.register_blueprint(bd_login)
app.register_blueprint(pedido_bp, url_prefix='/pedido')
app.register_blueprint(admin_bp, url_prefix='/admin') 

if __name__ == "__main__":
    port_render = int(os.environ.get("PORT", app.config['PORT']))
    
    app.run(
        host=app.config['HOST'], 
        port=port_render, 
        debug=app.config['DEBUG']
    )