from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import os

app = Flask(__name__, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)

# carrega configuração da pasta instance (opcional, não commitar)
app.config.from_pyfile('config.py', silent=True)

# DATABASE_URL esperado no ambiente, ex: postgres://user:pass@host:5432/db
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    # fallback para sqlite dentro da pasta instance (dev local)
    db_path = os.path.join(app.instance_path, 'beluxis.db')
    database_url = f"sqlite:///{db_path}"

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from .models import Cliente
    return Cliente.query.get(int(user_id))

from . import routes  # noqa: F401
