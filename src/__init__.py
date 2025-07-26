"""
Module d'initialisation de l'application Flask
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

# Créer l'instance Flask
app = Flask(__name__)

# Charger la configuration
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.py')
app.config.from_pyfile(config_path)

# Initialiser les extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuration Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Connecter vous pour acceder a cette page!!!😜"

# Importer les modules après l'initialisation
from . import models
from . import utilis
from . import admin