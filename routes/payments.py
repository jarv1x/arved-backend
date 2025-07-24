from flask import Blueprint, jsonify

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/", methods=["GET"])
def get_payments():
    return jsonify({"message": "Payments API is working"}), 200
  