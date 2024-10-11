from flask import Blueprint, request, jsonify
from models.post.post_model import PostSapiens
from extensions import db

post_bp = Blueprint('post', __name__)

@post_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()  # Obtener los datos JSON enviados desde el formulario

    # Validar los datos
    if not data or not data.get('post_name') or not data.get('post_description'):
        return jsonify({'message': 'Missing data'}), 400

    # Crear un nuevo post
    new_post = PostSapiens(
        post_name=data['post_name'],
        post_description=data['post_description']
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({'message': 'Post created successfully'}), 201
