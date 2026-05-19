from flask import Blueprint, jsonify
from apps.lanche.model_lanche import listarLanche

bd_Lanche = Blueprint('Lanche', __name__)

@bd_Lanche.route("/lanche", methods=["GET"])
def listar_lanche_publico():
    try:
        lanches_lista = listarLanche()
        return jsonify(lanches_lista), 200
    except Exception as e:
        return jsonify({"Erro": f"Erro interno: {str(e)}"}), 500