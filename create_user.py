#!/usr/bin/env python3
"""Script pour créer l'utilisateur de test nuur"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import User, db
from werkzeug.security import generate_password_hash
from src import app

def create_test_user():
    with app.app_context():
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username='nuur').first()
        
        if existing_user:
            print("L'utilisateur 'nuur' existe déjà")
            print(f"Statut actuel: {existing_user.statut}")
            print(f"Rôle actuel: {existing_user.role}")
            
            # Mettre à jour le mot de passe au cas où
            existing_user.password = generate_password_hash('nuur2003')
            existing_user.statut = 'ACTIF'
            existing_user.role = 'USER'
            db.session.commit()
            print("Mot de passe mis à jour avec 'nuur2003'")
        else:
            # Créer un nouvel utilisateur
            hashed_password = generate_password_hash('nuur2003')
            new_user = User(
                username='nuur', 
                password=hashed_password, 
                statut='ACTIF', 
                role='USER'
            )
            db.session.add(new_user)
            db.session.commit()
            print("Utilisateur 'nuur' créé avec succès!")
            print("Username: nuur")
            print("Password: nuur2003")
            print("Statut: ACTIF")
            print("Rôle: USER")

        # Créer aussi un admin si nécessaire
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            hashed_admin_password = generate_password_hash('admin123')
            admin_user = User(
                username='admin',
                password=hashed_admin_password,
                statut='ACTIF',
                role='ADMIN'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Utilisateur admin créé avec succès!")
            print("Username: admin")
            print("Password: admin123")

if __name__ == '__main__':
    create_test_user()
