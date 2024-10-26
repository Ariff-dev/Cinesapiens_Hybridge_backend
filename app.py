from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from extensions import db  

# Importar blueprints
from routes.user_routes import user_bp
from routes.post_routes import post_bp
from routes.comments_routes import comment_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from config import *



app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cinesapiens:cinesapines2024@192.168.100.22:5432/cinesapiens_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'Dedica88'  

# Habilitar CORS para todas las rutas
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializar la base de datos, migraciones y JWT
db.init_app(app)
migrate = Migrate(app, db) 
jwt = JWTManager(app)

# Registrar los Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# Manejo de errores (opcional)
@app.errorhandler(500)
def handle_500_error(e):
    return {'message': 'Internal Server Error'}, 500

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
