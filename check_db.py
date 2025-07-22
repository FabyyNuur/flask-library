#!/usr/bin/env python3
"""Script pour vérifier l'état de la base de données"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import User, Panier, PanierItem, Livres, db
from src import app

def check_database():
    with app.app_context():
        print("=== Vérification de la base de données ===")
        
        # Vérifier les utilisateurs
        users = User.query.all()
        print(f"Nombre d'utilisateurs: {len(users)}")
        for user in users:
            print(f"  - {user.username} (ID: {user.id}, Statut: {user.statut}, Rôle: {user.role})")
        
        # Vérifier les livres
        livres = Livres.query.all()
        print(f"\nNombre de livres: {len(livres)}")
        for livre in livres[:5]:  # Afficher seulement les 5 premiers
            print(f"  - {livre.title} (ID: {livre.id}, Prix: {livre.prix})")
        
        # Vérifier les paniers
        paniers = Panier.query.all()
        print(f"\nNombre de paniers: {len(paniers)}")
        for panier in paniers:
            print(f"  - Panier {panier.id} pour utilisateur {panier.user_id}, validé: {panier.valide}, articles: {len(panier.items)}")
            for item in panier.items:
                if item.livre:
                    print(f"    * {item.livre.title} x{item.nombre}")
                else:
                    print(f"    * Livre ID {item.livre_id} (MANQUANT) x{item.nombre}")

if __name__ == '__main__':
    check_database()
