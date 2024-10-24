from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializar la instancia de SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()