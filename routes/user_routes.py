from flask import Blueprint, request, jsonify
from models.user.user_model import UserSapiens
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity


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



@user_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_sapiens():
    current_user = get_jwt_identity()  # Obtiene el dict
    current_user_id = current_user['id']  # Ajusta esto según la estructura de tu dict


    user = UserSapiens.query.get(int(current_user_id))

    if user is None:
        return jsonify({'message': 'User not found.'}), 404

    if user.apply == 1:
        return jsonify({'message': 'Ya haz aplicado a ser sapiens y tu solicitud esta en revisión.'}), 400
    
    user.apply = 1
    db.session.commit()

    return jsonify({'message': 'Tu solicitud para ser sapiens ha sido recibida.'}), 200



