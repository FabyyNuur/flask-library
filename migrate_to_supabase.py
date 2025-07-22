#!/usr/bin/env python3
"""
Script pour migrer les données SQLite vers Supabase PostgreSQL
"""
import sys
import os
import sqlite3

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath('.'))

def migrate_sqlite_to_supabase():
    """Migre les données de SQLite vers Supabase"""
    
    print("🔄 Migration SQLite → Supabase PostgreSQL")
    print("=" * 50)
    
    # Vérifier si la base SQLite existe
    sqlite_path = 'bookstore.sqlite'
    if not os.path.exists(sqlite_path):
        print("❌ Base de données SQLite non trouvée")
        print("ℹ️  Création d'une nouvelle base Supabase...")
        create_fresh_supabase_db()
        return
    
    try:
        # Configuration temporaire pour Supabase
        os.environ['DATABASE_URL'] = input("📝 Entrez votre DATABASE_URL Supabase: ")
        
        # Import après configuration des variables d'environnement
        from app import app
        app.config.from_pyfile('config_supabase.py')
        
        from src.models import db, User, Livres, Panier, LigneCommande
        
        print("✅ Connexion à Supabase établie")
        
        with app.app_context():
            # Créer toutes les tables dans Supabase
            print("🏗️  Création des tables dans Supabase...")
            db.create_all()
            
            # Lire les données SQLite
            sqlite_conn = sqlite3.connect(sqlite_path)
            sqlite_conn.row_factory = sqlite3.Row
            
            # Migrer les utilisateurs
            print("👥 Migration des utilisateurs...")
            cursor = sqlite_conn.execute("SELECT * FROM user")
            users = cursor.fetchall()
            
            for user_row in users:
                existing_user = User.query.filter_by(username=user_row['username']).first()
                if not existing_user:
                    user = User(
                        username=user_row['username'],
                        password=user_row['password'],
                        role=user_row.get('role', 'USER'),
                        statut=user_row.get('statut', 'ACTIF')
                    )
                    db.session.add(user)
            
            db.session.commit()
            print(f"✅ {len(users)} utilisateurs migrés")
            
            # Migrer les livres
            print("📚 Migration des livres...")
            cursor = sqlite_conn.execute("SELECT * FROM livres")
            livres = cursor.fetchall()
            
            for livre_row in livres:
                existing_livre = Livres.query.filter_by(titre=livre_row['titre']).first()
                if not existing_livre:
                    livre = Livres(
                        titre=livre_row['titre'],
                        auteur=livre_row['auteur'],
                        prix=livre_row['prix'],
                        description=livre_row.get('description', ''),
                        image_url=livre_row.get('image_url', ''),
                        stock=livre_row.get('stock', 1)
                    )
                    db.session.add(livre)
            
            db.session.commit()
            print(f"✅ {len(livres)} livres migrés")
            
            sqlite_conn.close()
            
        print("\n🎉 Migration terminée avec succès !")
        print("📋 Prochaines étapes :")
        print("   1. Testez votre application avec Supabase")
        print("   2. Configurez les variables sur Vercel")
        print("   3. Déployez avec les nouvelles configurations")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        import traceback
        traceback.print_exc()

def create_fresh_supabase_db():
    """Crée une nouvelle base de données Supabase avec des données par défaut"""
    
    try:
        os.environ['DATABASE_URL'] = input("📝 Entrez votre DATABASE_URL Supabase: ")
        
        from app import app
        app.config.from_pyfile('config_supabase.py')
        from src.models import db, User, Livres
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            print("🏗️  Création des tables...")
            db.create_all()
            
            # Créer un utilisateur admin
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='ADMIN',
                statut='ACTIF'
            )
            db.session.add(admin)
            
            # Créer quelques livres d'exemple
            livres_exemples = [
                {
                    'titre': 'Python pour les débutants',
                    'auteur': 'Jean Dupont',
                    'prix': 29.99,
                    'description': 'Apprenez Python facilement',
                    'stock': 10
                },
                {
                    'titre': 'Flask Web Development',
                    'auteur': 'Miguel Grinberg',
                    'prix': 45.50,
                    'description': 'Guide complet pour Flask',
                    'stock': 5
                }
            ]
            
            for livre_data in livres_exemples:
                livre = Livres(**livre_data)
                db.session.add(livre)
            
            db.session.commit()
            
            print("✅ Base de données Supabase créée avec succès !")
            print("👤 Utilisateur admin créé: admin/admin123")
            print(f"📚 {len(livres_exemples)} livres d'exemple ajoutés")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("🔄 Assistant de Migration Supabase")
    print("=" * 40)
    
    choice = input("""
Choisissez une option:
1. Migrer données SQLite → Supabase
2. Créer nouvelle base Supabase
3. Annuler

Votre choix (1-3): """)
    
    if choice == '1':
        migrate_sqlite_to_supabase()
    elif choice == '2':
        create_fresh_supabase_db()
    else:
        print("👋 Migration annulée")
