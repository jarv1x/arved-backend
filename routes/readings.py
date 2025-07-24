from flask import Blueprint, jsonify

readings_bp = Blueprint("readings", __name__)

@readings_bp.route("/", methods=["GET"])
def get_readings():
    return jsonify({"message": "Readings API is working"}), 200
