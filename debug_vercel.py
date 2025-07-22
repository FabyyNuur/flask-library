# pylint: disable=broad-exception-caught
#!/usr/bin/env python3
"""Script de debug pour tester la configuration Vercel localement."""

import sys
import os
import traceback

print("=== Debug Vercel ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    print("\n1. Test import de app.py...")
    from app import app
    print("✓ Import de app réussi")
    
    print(f"✓ Routes disponibles: {[rule.rule for rule in app.url_map.iter_rules()]}")
    
    print("\n2. Test de la configuration...")
    print(f"✓ DEBUG: {app.config.get('DEBUG')}")
    print(f"✓ SECRET_KEY défini: {'SECRET_KEY' in app.config}")
    print(f"✓ SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    print("\n3. Test des imports des modèles...")
    from src.models import db, User, Livres
    print("✓ Import des modèles réussi")
    
    print("\n4. Test du contexte de l'app...")
    with app.app_context():
        print("✓ Contexte de l'app créé")
        try:
            db.create_all()
            print("✓ Tables créées/vérifiées")
        except Exception as e:
            print(f"⚠ Erreur création tables: {e}")
    
    print("\n5. Test de la route racine...")
    with app.test_client() as client:
        response = client.get('/')
        print(f"✓ Status code: {response.status_code}")
        if response.status_code != 200:
            print(f"⚠ Réponse: {response.data.decode()}")
    
    print("\n✅ Tous les tests sont passés !")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    print(f"Traceback complet:")
    traceback.print_exc()
    sys.exit(1)
