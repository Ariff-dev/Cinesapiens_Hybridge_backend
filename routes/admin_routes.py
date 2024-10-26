from flask import Blueprint, request, jsonify
from models.user.user_model import UserSapiens
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('user', __name__)

@admin_bp.route('/active-users', methods=['GET'])
@jwt_required()
def active_users():
    users = UserSapiens.query.filter_by(apply=2).all()  # Filtrar usuarios que están activos
    result = [
        {'id': user.id_user, 'username': user.username, 'email': user.email}
        for user in users
    ]
    return jsonify(result), 200


@admin_bp.route('/sapiens-applications', methods=['GET'])
@jwt_required()
def sapiens_applications():
    current_user = get_jwt_identity()  # Obtener el ID del usuario actual
    users = UserSapiens.query.filter_by(apply=1).all()  # Filtrar usuarios que han aplicado
    result = [
        {'id': user.id_user, 'username': user.username, 'email': user.email} 
        for user in users
    ]
    
    return jsonify(result), 200

@admin_bp.route('/deny-application/<int:user_id>', methods=['PUT'])
@jwt_required()
def deny_application(user_id):
    user = UserSapiens.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user.apply = 0  # Cambiar apply a 0
    db.session.commit()
    return jsonify({'message': f'Application for {user.username} denied'}), 200


@admin_bp.route('/promote-application/<int:user_id>', methods=['PUT'])
@jwt_required()
def promote_application(user_id):
    user = UserSapiens.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.apply = 2  # Cambiar apply a 2
    user.user_role = 'sapiens'  # Cambiar el rol a sapiens
    db.session.commit()
    return jsonify({'message': f'User {user.username} promoted to sapiens'}), 200


@admin_bp.route('/descend-application/<int:user_id>', methods=['PUT'])
@jwt_required()
def descend_application(user_id):
    user = UserSapiens.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.apply = 0  # Cambiar el estado a standard
    db.session.commit()  # Guardar los cambios en la base de datos

    return jsonify({'message': 'User has been descended to standard'}), 200



