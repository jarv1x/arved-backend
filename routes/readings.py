import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, Reading
from utils import allowed_file

# *** Defineeri Blueprint kõige alguses ***
readings_bp = Blueprint('readings', __name__)

# *** Failide salvestamise kaust ***
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

    print("DEBUG FORM:", dict(request.form))
    print("DEBUG FILES:", request.files)

    # Kontroll, et kõik väljad oleks täidetud
    if not reading_value or not date_str or not apartment_id or not file:
        return jsonify({'error': 'Kõik väljad on kohustuslikud'}), 400

    # Failitüübi kontroll
    if not allowed_file(file.filename):
        return jsonify({'error': 'Faili tüüp pole lubatud'}), 400

    # Kuupäeva formaat
    try:
        if '.' in date_str:
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
        else:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': f'Vale kuupäeva formaat: {date_str}'}), 400

    # Näidu väärtuse kontroll
    try:
        reading_value = float(reading_value)
    except ValueError:
        return jsonify({'error': f'Vale näidu väärtus: {reading_value}'}), 400

    # Korteri ID kontroll
    try:
        apartment_id = int(apartment_id)
    except ValueError:
        return jsonify({'error': f'Vale korteri ID: {apartment_id}'}), 400

    # Salvestame faili
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Salvestame kirje andmebaasi
    reading = Reading(
        reading_value=reading_value,
        date=date,
        apartment_id=apartment_id,
        file_path=filepath,
        user_id=user_id
    )

    db.session.add(reading)
    db.session.commit()

    return jsonify({'message': 'Veenäit salvestatud edukalt'}), 201
