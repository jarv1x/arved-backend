
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = os.getenv('JWT_SECRET', 'supersecret')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 400

    hashed_pw = generate_password_hash(data['password'])
    user = User(email=data['email'], password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not check_password_hash(user.password_hash, data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
        SECRET_KEY, algorithm='HS256'
    )
    return jsonify({'token': token})
