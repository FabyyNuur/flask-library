#!/usr/bin/env python3
"""Script pour nettoyer et tester les paniers"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import User, Panier, PanierItem, Livres, db
from src import app

def clean_and_test():
    with app.app_context():
        print("=== Nettoyage et test des paniers ===")
        
        # Trouver l'utilisateur nuur
        nuur = User.query.filter_by(username='nuur').first()
        if not nuur:
            print("Utilisateur 'nuur' non trouvé")
            return
            
        print(f"Utilisateur: {nuur.username} (ID: {nuur.id})")
        
        # Afficher les paniers actuels
        paniers = Panier.query.filter_by(user_id=nuur.id).all()
        print(f"Paniers actuels pour {nuur.username}: {len(paniers)}")
        
        for panier in paniers:
            print(f"  - Panier {panier.id}: validé={panier.valide}, articles={len(panier.items)}")
            
        # Trouver le panier non validé le plus récent
        panier_actuel = Panier.query.filter_by(user_id=nuur.id, valide=False).order_by(Panier.id.desc()).first()
        
        if panier_actuel:
            print(f"Panier actuel non validé: {panier_actuel.id}")
            print(f"Articles dans le panier actuel:")
            for item in panier_actuel.items:
                if item.livre:
                    print(f"  - {item.livre.title} x{item.nombre} = {item.livre.prix * item.nombre}€")
                else:
                    print(f"  - Livre ID {item.livre_id} (MANQUANT) x{item.nombre}")
        else:
            print("Aucun panier non validé trouvé - c'est normal après une commande")
            
        print("\n=== Test terminé ===")

if __name__ == '__main__':
    clean_and_test()
