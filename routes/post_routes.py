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


@post_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = PostSapiens.query.all()  # O la lógica que uses para obtener las publicaciones
    return jsonify([{
        'id_post_sa': post.id_post_sa,
        'post_name': post.post_name,
        'post_description': post.post_description,
        'image_url': post.image_url
    } for post in posts])



@post_bp.route('/edit-post/<int:post_id>', methods=['PUT'])
@jwt_required()
def edit_post(post_id):
    try:
        # Obtener la identidad del usuario
        current_user = get_jwt_identity()
        print("Current user:", current_user)  # Para depurar

        # Si current_user es un diccionario, accede al ID así:
        user_id = current_user if isinstance(current_user, int) else current_user['id']

        # Verificar que el usuario exista y tenga el rol adecuado
        user = UserSapiens.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404

        if user.user_role != 'sapiens':
            return jsonify({'message': 'Access denied, only sapiens can edit posts.'}), 403

        # Obtener los nuevos datos del request
        post_name = request.form.get('post_name')
        post_description = request.form.get('post_description')
        file = request.files.get('image')

        # Buscar el post por ID
        post = PostSapiens.query.get(post_id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        # Actualizar campos según los datos enviados
        if post_name:
            post.post_name = post_name
        if post_description:
            post.post_description = post_description
        if file:
            upload_result = cloudinary.uploader.upload(file)
            post.image_url = upload_result['secure_url']

        # Guardar los cambios
        db.session.commit()

        return jsonify({'message': 'Post updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@post_bp.route('/delete-post/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        current_user = get_jwt_identity()
        print("Current user:", current_user)  # Para depurar

        # Si current_user es un diccionario, accede al ID así:
        user_id = current_user if isinstance(current_user, int) else current_user['id']

        user = UserSapiens.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404

        if user.user_role != 'sapiens':
            return jsonify({'message': 'Access denied, only sapiens can delete posts.'}), 403
        
        post = PostSapiens.query.get(post_id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        db.session.delete(post)
        db.session.commit()

        return jsonify({'message': 'Post deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


