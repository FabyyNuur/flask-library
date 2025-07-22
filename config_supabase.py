"""
Configuration pour Supabase PostgreSQL
"""
import os

# Configuration de base
DEBUG = False
TESTING = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'NurulHalbiii-Supabase-Production-2025')

# Configuration Supabase PostgreSQL
# Format: postgresql://postgres:[password]@db.[project-id].supabase.co:5432/postgres
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    # Convertir postgres:// en postgresql:// pour SQLAlchemy 2.x
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///:memory:'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_timeout': 20,
    'pool_recycle': -1,
    'pool_pre_ping': True,
    'pool_size': 10,
    'max_overflow': 20
}

# Sécurité
USE_SESSION_FOR_NEXT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Configuration Flask-Login
LOGIN_MESSAGE = "Connectez-vous pour accéder à cette page !"

# Configuration pour Vercel
WTF_CSRF_ENABLED = False  # Désactiver CSRF pour les API Vercel
