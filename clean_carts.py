#!/usr/bin/env python3
"""Script pour nettoyer les paniers multiples non validés"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import User, Panier, PanierItem, Livres, db
from src import app

def clean_multiple_carts():
    with app.app_context():
        print("=== Nettoyage des paniers multiples ===")
        
        # Trouver tous les utilisateurs ayant plusieurs paniers non validés
        users_with_multiple_carts = []
        
        all_users = User.query.all()
        for user in all_users:
            paniers_non_valides = Panier.query.filter_by(user_id=user.id, valide=False).all()
            if len(paniers_non_valides) > 1:
                users_with_multiple_carts.append((user, paniers_non_valides))
        
        print(f"Utilisateurs avec paniers multiples: {len(users_with_multiple_carts)}")
        
        for user, paniers in users_with_multiple_carts:
            print(f"\nUtilisateur: {user.username} (ID: {user.id})")
            print(f"Paniers non validés: {[p.id for p in paniers]}")
            
            # Garder le premier panier et fusionner les autres
            panier_principal = paniers[0]
            print(f"Panier principal: {panier_principal.id}")
            
            for autre_panier in paniers[1:]:
                print(f"Fusion du panier {autre_panier.id} dans {panier_principal.id}")
                
                # Transférer tous les articles
                for item in autre_panier.items:
                    existing_item = PanierItem.query.filter_by(
                        panier_id=panier_principal.id, 
                        livre_id=item.livre_id
                    ).first()
                    
                    if existing_item:
                        print(f"  - Livre {item.livre_id}: {existing_item.nombre} + {item.nombre} = {existing_item.nombre + item.nombre}")
                        existing_item.nombre += item.nombre
                    else:
                        print(f"  - Transfert livre {item.livre_id} x{item.nombre}")
                        item.panier_id = panier_principal.id
                
                # Supprimer l'ancien panier
                db.session.delete(autre_panier)
                print(f"  - Panier {autre_panier.id} supprimé")
            
            # Calculer le nouveau total
            panier_principal.total = sum(
                item.livre.prix * item.nombre 
                for item in panier_principal.items 
                if item.livre
            )
            
            print(f"Nouveau total du panier {panier_principal.id}: {panier_principal.total}€")
        
        # Sauvegarder tous les changements
        db.session.commit()
        
        print("\n=== Vérification finale ===")
        
        # Vérifier le résultat
        for user in User.query.all():
            paniers_non_valides = Panier.query.filter_by(user_id=user.id, valide=False).all()
            if len(paniers_non_valides) > 1:
                print(f"ERREUR: {user.username} a encore {len(paniers_non_valides)} paniers")
            elif len(paniers_non_valides) == 1:
                panier = paniers_non_valides[0]
                print(f"✅ {user.username}: 1 panier (ID: {panier.id}, {len(panier.items)} articles)")
            else:
                print(f"✅ {user.username}: aucun panier actif")
        
        print("\n=== Nettoyage terminé ===")

if __name__ == '__main__':
    clean_multiple_carts()
