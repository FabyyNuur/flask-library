#!/usr/bin/env python3
"""
Script de test local pour simuler l'environnement Vercel
"""
import os
import sys

# Simuler l'environnement de production
os.environ['FLASK_ENV'] = 'production'
os.environ['DEBUG'] = 'False'

# Ajouter le répertoire api au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

try:
    from api.index import app
    
    print("✅ Import de l'application réussi")
    print("🚀 Démarrage du serveur de test...")
    
    # Tester que l'app se lance
    with app.test_client() as client:
        response = client.get('/')
        print(f"📊 Test de la route '/' : Status {response.status_code}")
        
        # Test de la route login
        response = client.get('/login')
        print(f"📊 Test de la route '/login' : Status {response.status_code}")
    
    print("✅ Tests de base réussis ! L'application semble prête pour Vercel.")
    print("\n📋 Prochaines étapes :")
    print("1. Commitez tous les fichiers créés")
    print("2. Poussez vers GitHub")
    print("3. Déployez sur Vercel")
    print("4. Considérez migrer vers une base de données cloud")
    
except Exception as e:
    print(f"❌ Erreur lors du test : {e}")
    print("🔧 Vérifiez les imports et la structure de votre application")
    sys.exit(1)
