from flask import Blueprint, request, jsonify
from models.user.user_model import UserSapiens
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('user', __name__)



@admin_bp.route('/sapiens-applications', methods=['GET'])
@jwt_required()
def sapiens_applications():
    users = UserSapiens.query.filter_by(apply=1).all()  # Filtrar usuarios que han aplicado
    result = [
        {'id': user.id_user, 'username': user.username, 'email': user.email} 
        for user in users
    ]
    return jsonify(result), 200
