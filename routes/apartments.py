from flask import Blueprint, jsonify
from models import Apartment

apartments_bp = Blueprint('apartments', __name__)

@apartments_bp.route('/apartments', methods=['GET'])
def get_apartments():
    apartments = Apartment.query.all()
    return jsonify([{"id": apt.id, "name": apt.name} for apt in apartments])
