from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from models import db, Upload
from datetime import datetime

invoices_bp = Blueprint('invoices', __name__)

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ✅ Faili üleslaadimine
@invoices_bp.route('/upload-invoice', methods=['POST'])
def upload_invoice():
    if 'file' not in request.files:
        return jsonify({'error': 'Faili ei saadetud'}), 400

    file = request.files['file']
    category = request.form.get('category')
    invoice_date = request.form.get('invoice_date')
    invoice_number = request.form.get('invoice_number')
    amount = request.form.get('amount')
    quantity = request.form.get('quantity')
    unit = request.form.get('unit')
    price = request.form.get('price')
    vat = request.form.get('vat')
    reading_value = request.form.get('reading_value')
    apartment = request.form.get('apartment')

    if file.filename == '':
        return jsonify({'error': 'Faili nimi on tühi'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        new_upload = Upload(
            category=category,
            file_name=filename,
            original_name=file.filename,
            upload_date=datetime.utcnow(),
            invoice_date=datetime.strptime(invoice_date, "%d.%m.%Y") if invoice_date else None,
            invoice_number=invoice_number,
            amount=float(amount.replace(',', '.')) if amount else None,
            quantity=float(quantity.replace(',', '.')) if quantity else None,
            unit=unit,
            price=float(price.replace(',', '.')) if price else None,
            vat=float(vat.replace(',', '.')) if vat else 24,
            reading_value=float(reading_value.replace(',', '.')) if reading_value else None,
            apartment=apartment
        )

        db.session.add(new_upload)
        db.session.commit()

        return jsonify({
            'message': 'Fail edukalt üles laetud',
            'filename': filename,
            'path': save_path
        }), 200

    return jsonify({'error': 'Vale faili tüüp'}), 400


# ✅ Üleslaaditud failide nimekiri
@invoices_bp.route('/list', methods=['GET'])
def list_invoices():
    uploads = Upload.query.order_by(Upload.upload_date.desc()).all()
    data = [
        {
            'id': u.id,
            'file_name': u.file_name,
            'category': u.category,
            'invoice_date': u.invoice_date.strftime("%d.%m.%Y") if u.invoice_date else "",
            'upload_date': u.upload_date.strftime("%d.%m.%Y"),
            'download_url': f"/invoices/download/{u.id}"
        }
        for u in uploads
    ]
    return jsonify(data)


# ✅ Faili allalaadimine
@invoices_bp.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    file = Upload.query.get(file_id)
    if not file:
        return jsonify({'error': 'Faili ei leitud'}), 404

    # Failitee ja nimi
    file_path = safe_join(UPLOAD_FOLDER, file.file_name)
    if not os.path.exists(file_path):
        return jsonify({'error': 'Fail puudub serveris'}), 404

    # Faili allalaadimine koos õigete päistega
    return send_from_directory(
        directory=UPLOAD_FOLDER,
        path=file.file_name,
        as_attachment=True,
        download_name=file.file_name
    )