from flask import Blueprint, request, jsonify
from models.post.post_model import PostSapiens
from models.user.user_model import UserSapiens
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import cloudinary

post_bp = Blueprint('post', __name__)

@post_bp.route('/create-post', methods=['POST'])
@jwt_required()
def create_post():
    current_user = get_jwt_identity()
    print(current_user)
    # Si current_user es un diccionario, extrae el ID
    if isinstance(current_user, dict):
        user_id = current_user.get('id')  # Ajusta esto según tu implementación
    else:
        user_id = int(current_user)  # Suponiendo que es un entero si no es un dict

    user = UserSapiens.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    
    if user.user_role != 'sapiens':
        return jsonify({'message': 'Access denied, only sapiens can create posts.'}), 403
    
    post_name = request.form.get('post_name')
    post_description = request.form.get('post_description')
    file = request.files.get('image')

    if not post_name or not post_description:
        return jsonify({'message': 'Missing data'}), 400

    # Si se ha enviado un archivo, subirlo a Cloudinary
    image_url = None
    if file:
        try:
            upload_result = cloudinary.uploader.upload(file)
            image_url = upload_result['secure_url']
        except Exception as e:
            return jsonify({'message': 'Failed to upload image', 'error': str(e)}), 500

    # Crear un nuevo post con la URL de la imagen
    new_post = PostSapiens(
        post_name=post_name,
        post_description=post_description,
        image_url=image_url
    )

    try:
        db.session.add(new_post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Revertir cualquier cambio en caso de error
        return jsonify({'message': 'Error creating post', 'error': str(e)}), 500

    return jsonify({'message': 'Post created successfully', 'post': {
        'name': post_name,
        'description': post_description,
        'image_url': image_url
    }}), 201
