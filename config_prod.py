import os

# Configuration pour la production (Vercel)
DEBUG = False
APP_NAME = "Nuur-Library"

# Pour Vercel, nous utiliserons des variables d'environnement
SECRET_KEY = os.environ.get('SECRET_KEY', 'NurulHalbiii')

# Base de données - en production, vous pourriez vouloir utiliser PostgreSQL ou MySQL
# Pour commencer, nous gardons SQLite mais avec un chemin absolu
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "sqlite:///" + os.path.join(basedir, "bookstore.sqlite"))

SQLALCHEMY_TRACK_MODIFICATIONS = False

NO_IMG = "https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg"

USE_SESSION_FOR_NEXT = True
