from flask import Blueprint, jsonify, request
from extensions import db
from models.user.user_model import UserSapiens

# Crear el Blueprint
user_bp = Blueprint('user_bp', __name__)

# Ejemplo de ruta GET para obtener todos los usuarios
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = UserSapiens.query.all()
    users_list = [{'id_user': user.id_user, 'username': user.username, 'email': user.email, 'user_role': user.user_role} for user in users]
    return jsonify(users_list)

# Ejemplo de ruta POST para crear un nuevo usuario
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = UserSapiens(
        username=data['username'],
        email=data['email'],
        user_password=data['user_password'],
        user_role=data.get('user_role', 'standard')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201
