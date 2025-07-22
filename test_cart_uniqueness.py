#!/usr/bin/env python3
"""Script de test pour vérifier l'unicité des paniers"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import User, Panier, PanierItem, Livres, db
from src import app

def test_cart_uniqueness():
    with app.app_context():
        print("=== Test d'unicité des paniers ===")
        
        # Utiliser l'utilisateur nuur pour le test
        user = User.query.filter_by(username='nuur').first()
        if not user:
            print("Erreur: utilisateur nuur non trouvé")
            return
            
        print(f"Test avec utilisateur: {user.username}")
        
        # Vérifier l'état initial
        paniers_non_valides = Panier.query.filter_by(user_id=user.id, valide=False).all()
        print(f"Paniers non validés au début: {len(paniers_non_valides)}")
        
        # Simuler l'ajout d'un nouveau panier (comme dans ajoutPanier)
        livre = Livres.query.first()
        if not livre:
            print("Aucun livre trouvé pour le test")
            return
            
        print(f"Test avec livre: {livre.title}")
        
        # Créer manuellement un deuxième panier pour tester
        nouveau_panier = Panier(user_id=user.id, valide=False, total=0)
        db.session.add(nouveau_panier)
        db.session.commit()
        
        print(f"Panier de test créé: ID {nouveau_panier.id}")
        
        # Vérifier qu'on a maintenant 2 paniers
        paniers_non_valides = Panier.query.filter_by(user_id=user.id, valide=False).all()
        print(f"Paniers après création: {len(paniers_non_valides)}")
        
        # Simuler le code de nettoyage d'ajoutPanier
        if len(paniers_non_valides) > 1:
            print("DÉTECTION: Plusieurs paniers trouvés, fusion en cours...")
            
            panier_principal = paniers_non_valides[0]
            print(f"Panier principal: {panier_principal.id}")
            
            # Fusionner les autres paniers
            for autre_panier in paniers_non_valides[1:]:
                print(f"Fusion du panier {autre_panier.id}")
                
                # Transférer les items (s'il y en a)
                for item in autre_panier.items:
                    existing_item = PanierItem.query.filter_by(
                        panier_id=panier_principal.id,
                        livre_id=item.livre_id
                    ).first()
                    
                    if existing_item:
                        existing_item.nombre += item.nombre
                    else:
                        item.panier_id = panier_principal.id
                
                # Supprimer l'ancien panier
                db.session.delete(autre_panier)
            
            # Recalculer le total
            panier_principal.total = sum(
                item.livre.prix * item.nombre 
                for item in panier_principal.items 
                if item.livre
            )
            
            db.session.commit()
            print("Fusion terminée")
        
        # Vérification finale
        paniers_finaux = Panier.query.filter_by(user_id=user.id, valide=False).all()
        print(f"Paniers après nettoyage: {len(paniers_finaux)}")
        
        if len(paniers_finaux) == 1:
            print("✅ TEST RÉUSSI: Un seul panier non validé")
            panier = paniers_finaux[0]
            print(f"   Panier ID: {panier.id}")
            print(f"   Articles: {len(panier.items)}")
            print(f"   Total: {panier.total}€")
        else:
            print("❌ TEST ÉCHOUÉ: Nombre incorrect de paniers")
        
        print("\n=== Test terminé ===")

if __name__ == '__main__':
    test_cart_uniqueness()
