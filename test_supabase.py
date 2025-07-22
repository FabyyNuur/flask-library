#!/usr/bin/env python3
"""
Script de test pour la connexion Supabase
"""
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath('.'))

def test_supabase_connection():
    """Teste la connexion à Supabase"""
    
    print("🧪 Test de connexion Supabase")
    print("=" * 40)
    
    # Demander les informations de connexion
    if not os.environ.get('DATABASE_URL'):
        database_url = input("🔗 Entrez votre DATABASE_URL Supabase: ")
        os.environ['DATABASE_URL'] = database_url
    
    try:
        # Configuration
        print("⚙️  Configuration de l'application...")
        from app import app
        
        # Configurer directement sans fichier
        app.config.update({
            'DEBUG': False,
            'TESTING': False,
            'SECRET_KEY': 'NurulHalbiii-Supabase-Production-2025',
            'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_ENGINE_OPTIONS': {
                'pool_timeout': 20,
                'pool_recycle': -1,
                'pool_pre_ping': True,
                'pool_size': 10,
                'max_overflow': 20
            }
        })
        
        print(f"✅ Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')[:50]}...")
        
        # Test de connexion
        print("🔌 Test de connexion à la base de données...")
        from src.models import db, User, Livres
        
        with app.app_context():
            # Test de création des tables
            print("🏗️  Test de création des tables...")
            db.create_all()
            print("✅ Tables créées/vérifiées")
            
            # Test d'insertion
            print("✍️  Test d'écriture...")
            test_user = User.query.filter_by(username='test_supabase').first()
            if not test_user:
                from werkzeug.security import generate_password_hash
                test_user = User(
                    username='test_supabase',
                    password=generate_password_hash('test123'),
                    role='USER',
                    statut='ACTIF'
                )
                db.session.add(test_user)
                db.session.commit()
                print("✅ Utilisateur test créé")
            else:
                print("✅ Utilisateur test trouvé")
            
            # Test de lecture
            print("📖 Test de lecture...")
            users_count = User.query.count()
            livres_count = Livres.query.count()
            
            print(f"✅ {users_count} utilisateurs trouvés")
            print(f"✅ {livres_count} livres trouvés")
            
            # Nettoyage
            if test_user.username == 'test_supabase':
                db.session.delete(test_user)
                db.session.commit()
                print("🧹 Utilisateur test supprimé")
        
        print("\n🎉 Test Supabase réussi !")
        print("✅ Votre application est prête à utiliser Supabase")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion: {e}")
        
        # Conseils de résolution
        print("\n🔧 Conseils de résolution :")
        print("1. Vérifiez votre DATABASE_URL")
        print("2. Vérifiez que votre projet Supabase est actif")
        print("3. Vérifiez votre mot de passe de base de données")
        print("4. Installez les dépendances: pip install psycopg2-binary supabase")
        
        import traceback
        print(f"\nDétails de l'erreur:")
        traceback.print_exc()
        
        return False

if __name__ == '__main__':
    success = test_supabase_connection()
    
    if success:
        print("\n🚀 Prochaines étapes :")
        print("1. Migrez vos données: python migrate_to_supabase.py")
        print("2. Configurez Vercel: ./setup_vercel_env.sh")
        print("3. Déployez: vercel --prod")
    else:
        print("\n❌ Résolvez les erreurs avant de continuer")
        sys.exit(1)
