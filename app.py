from flask import Flask
from extensions import db  # Importar db desde el nuevo archivo extensions
from routes.user_routes import user_bp

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cinesapiens:cinesapiens2024@192.168.100.22:5432/cinesapiens-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Registrar el Blueprint para las rutas de usuario
from routes.user_routes import user_bp
from routes.post_routes import post_bp
from routes.comments_routes import comment_bp

app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(comment_bp)




# Crear las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
