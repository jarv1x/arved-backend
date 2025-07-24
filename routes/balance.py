from flask import Blueprint, jsonify

balance_bp = Blueprint("balance", __name__)

@balance_bp.route("/", methods=["GET"])
def get_balance():
    return jsonify({"message": "Balance calculation placeholder"}), 200
