import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Reading
from utils import allowed_file
from datetime import datetime

readings_bp = Blueprint('readings', __name__)
UPLOAD_FOLDER = 'uploads/readings'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@readings_bp.route('/upload-reading', methods=['POST'])
@jwt_required()
def upload_reading():
    user_id = get_jwt_identity()
    reading_value = request.form.get('reading')
    date_str = request.form.get('date')
    apartment_id = request.form.get('apartment_id')
    file = request.files.get('file')

    # Kontrollime, et kõik väljad on olemas
    if not reading_value or not date_str or not apartment_id or not file:
        return jsonify({'error': 'Kõik väljad on kohustuslikud'}), 400

    # Faili kontroll
    if not allowed_file(file.filename):
        return jsonify({'error': 'Faili tüüp pole lubatud'}), 400

    # Kuupäeva formaat
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Vale kuupäeva formaat'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Salvesta DB-sse
    reading = Reading(
        reading_value=float(reading_value),
        date=date,
        apartment_id=int(apartment_id),
        file_path=filepath,
        user_id=user_id
    )
    db.session.add(reading)
    db.session.commit()

    return jsonify({'message': 'Veenäit salvestatud edukalt'}), 201
