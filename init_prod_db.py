"""
Script d'initialisation de la base de données pour la production
Ce script peut être utilisé pour initialiser une nouvelle base de données sur Vercel
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import db, User, Livres, Categorie
from src import app
from werkzeug.security import generate_password_hash

def init_production_db():
    """Initialise la base de données pour la production"""
    
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        
        # Créer un utilisateur admin par défaut
        admin_exists = User.query.filter_by(username='admin').first()
        if not admin_exists:
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin123'),  # Changez ce mot de passe !
                role='ADMIN',
                statut='ACTIF'
            )
            db.session.add(admin_user)
        
        # Créer quelques catégories par défaut
        if not Categorie.query.first():
            categories = [
                'Fiction', 'Non-Fiction', 'Science', 'Histoire', 
                'Biographie', 'Poésie', 'Théâtre', 'Jeunesse'
            ]
            for cat_name in categories:
                categorie = Categorie(name=cat_name)
                db.session.add(categorie)
        
        # Commit les changements
        try:
            db.session.commit()
            print("✅ Base de données initialisée avec succès")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de l'initialisation : {e}")

if __name__ == '__main__':
    init_production_db()
