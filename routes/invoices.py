
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from models import db, Upload
from utils import allowed_file
from flask_jwt_extended import jwt_required, get_jwt_identity

invoices_bp = Blueprint('invoices', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@invoices_bp.route('/upload-invoice', methods=['POST'])
@jwt_required()
def upload_invoice():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        user_id = get_jwt_identity()
        upload = Upload(filename=filename, filepath=filepath, user_id=user_id)
        db.session.add(upload)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully'}), 201
    else:
        return jsonify({'error': 'Invalid file type'}), 400
