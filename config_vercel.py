"""
Configuration pour la production Vercel
"""
import os

# Configuration de base
DEBUG = False
TESTING = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'votre-secret-key-production-tres-securisee-changez-moi')

# Base de données - utiliser une base de données en mémoire pour Vercel
# ou une base de données externe comme PostgreSQL
if os.environ.get('DATABASE_URL'):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
else:
    # Base de données en mémoire pour les tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Sécurité
USE_SESSION_FOR_NEXT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Configuration Flask-Login
LOGIN_MESSAGE = "Connectez-vous pour accéder à cette page !"
