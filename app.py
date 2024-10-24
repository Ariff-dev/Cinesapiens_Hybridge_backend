from flask import Flask
from extensions import db  # Importar db desde el nuevo archivo extensions
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Importar para habilitar CORS
from flask_migrate import Migrate  # Importar Migrate directamente aquí

# Importar blueprints
from routes.user_routes import user_bp
from routes.post_routes import post_bp
from routes.comments_routes import comment_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cinesapiens:cinesapines2024@192.168.100.22:5432/cinesapiens_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clave secreta para JWT (ideal usar variables de entorno en producción)
app.config['JWT_SECRET_KEY'] = 'Dedica88'

# Inicializar la base de datos, migraciones y JWT
db.init_app(app)
migrate = Migrate(app, db)  # Inicializar Migrate aquí, relacionando la app y db
jwt = JWTManager(app)

# Habilitar CORS para todas las rutas
CORS(app)

# Registrar los Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(auth_bp)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
