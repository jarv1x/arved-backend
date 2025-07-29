from __init__ import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Upload(db.Model):
    __tablename__ = 'uploads'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Enum('vee_arve', 'prügi_arve', 'veenäit'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    invoice_date = db.Column(db.Date, nullable=True)
    invoice_number = db.Column(db.String(50), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=True)
    quantity = db.Column(db.Numeric(10, 2), nullable=True)
    unit = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    vat = db.Column(db.Numeric(5, 2), default=24.00)

    reading_value = db.Column(db.Numeric(10, 2), nullable=True)
    apartment = db.Column(db.String(50), nullable=True)

class Apartment(db.Model):
    __tablename__ = 'apartments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


