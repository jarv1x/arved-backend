from flask import Blueprint, jsonify

invoices_bp = Blueprint("invoices", __name__)

@invoices_bp.route("/", methods=["GET"])
def get_invoices():
    return jsonify({"message": "Invoices API is working"}), 200
