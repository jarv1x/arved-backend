from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

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

    # ✅ Oluline: identity -> user.id
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=24))


    return jsonify(access_token=access_token), 200
