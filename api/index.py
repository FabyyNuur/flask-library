"""
Point d'entrée pour le déploiement Vercel
"""
import sys
import os

# Ajouter le répertoire parent au path pour pouvoir importer les modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Configuration des variables d'environnement pour la production
os.environ['FLASK_ENV'] = 'production'

try:
    # Import de l'application principale
    from app import app
    
    # Configuration spécifique à Vercel
    config_path = os.path.join(parent_dir, 'config_vercel.py')
    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)
    else:
        # Configuration inline si le fichier n'existe pas
        app.config.update({
            'DEBUG': False,
            'TESTING': False,
            'SECRET_KEY': os.environ.get('SECRET_KEY', 'key-production-securisee'),
            'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL', 'sqlite:///:memory:'),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'USE_SESSION_FOR_NEXT': True,
        })
    
    # Forcer certaines configurations
    app.config.update({
        'DEBUG': False,
        'TESTING': False,
    })

    # Initialisation de la base de données dans le contexte de l'app
    with app.app_context():
        try:
            from src.models import db, User
            # Créer toutes les tables
            db.create_all()
            
            # Créer un utilisateur admin par défaut s'il n'existe pas
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                from werkzeug.security import generate_password_hash
                admin = User(
                    username='admin',
                    password=generate_password_hash('admin123'),
                    role='ADMIN',
                    statut='ACTIF'
                )
                db.session.add(admin)
                db.session.commit()
                print("Utilisateur admin créé")
                
        except Exception as db_error:
            print(f"Avertissement - Erreur base de données: {db_error}")

    # Handler principal pour Vercel
    def handler(request):
        """Handler principal pour les requêtes Vercel"""
        return app(request.environ, lambda status, headers: None)

except ImportError as import_error:
    print(f"Erreur d'import: {import_error}")
    # Fallback : créer une app Flask minimale
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error_page():
        return jsonify({
            "error": "Erreur de configuration",
            "message": str(import_error)
        }), 500

except Exception as general_error:
    print(f"Erreur générale: {general_error}")
    # Fallback : créer une app Flask minimale
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error_page():
        return jsonify({
            "error": "Erreur lors du démarrage",
            "message": str(general_error),
            "status": "error"
        }), 500

# Export final pour Vercel
# C'est ce que Vercel va chercher
app = app
