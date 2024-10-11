from flask import Blueprint, request, jsonify
from models.comment.comment_model import CommentPost
from extensions import db

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()  # Obtener los datos JSON enviados desde el formulario

    # Validar los datos
    if not data or not data.get('id_user') or not data.get('id_post_sa') or not data.get('comment_user_post'):
        return jsonify({'message': 'Missing data'}), 400

    # Crear un nuevo comentario
    new_comment = CommentPost(
        id_user=data['id_user'],
        id_post_sa=data['id_post_sa'],
        comment_user_post=data['comment_user_post']
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment created successfully'}), 201
