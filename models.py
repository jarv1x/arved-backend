from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Kasutaja mudel
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    uploads = db.relationship('Upload', backref='user', lazy=True)
    readings = db.relationship('Reading', backref='user', lazy=True)


# Korteri mudel
class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    readings = db.relationship('Reading', backref='apartment', lazy=True)


# Failide üleslaadimised
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Veenäidu mudel
class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reading_value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
