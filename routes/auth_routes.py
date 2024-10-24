# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from models.user.user_model import UserSapiens
from extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validar los datos
    if not data or not data.get('username') or not data.get('email') or not data.get('user_password'):
        return jsonify({'message': 'Missing data'}), 400

    # Verificar si el usuario ya existe
    if UserSapiens.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400

    # Crear un nuevo usuario
    new_user = UserSapiens(
        username=data['username'],
        email=data['email'],
        user_password=data['user_password']  # Aquí deberías usar un hash seguro
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validar los datos
    if not data or not data.get('email') or not data.get('user_password'):
        return jsonify({'message': 'Missing data'}), 400

    user = UserSapiens.query.filter_by(email=data['email'], user_password=data['user_password']).first()
    
    if not user:
        return jsonify({'message': 'Bad email or password'}), 401

    # Crear un token JWT
    access_token = create_access_token({'id': user.id_user, 'role': user.user_role})
    
    return jsonify(access_token=access_token), 200

@auth_bp.route('/promote/<int:user_id>', methods=['PUT'])
def promote_user(user_id):
    user = UserSapiens.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not Found'}), 404
    
    user.user_role = 'sapiens'
    db.session.commit()


    return jsonify({'message': f'User {user.username} promoted to sapiens'})

