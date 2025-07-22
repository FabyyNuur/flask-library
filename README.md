# 📚 Nuur-Library - Système de Gestion de Librairie en Ligne

Une application web moderne développée avec Flask pour la gestion d'une librairie en ligne, offrant une expérience complète pour les clients et les administrateurs.

## 🚀 Fonctionnalités

### 👤 Espace Client
- **Authentification** : Inscription, connexion et déconnexion sécurisées
- **Catalogue de livres** : Navigation et recherche dans le catalogue
- **Détails des livres** : Informations complètes (auteur, catégories, prix, description, etc.)
- **Panier d'achat** : Ajout/suppression d'articles, gestion des quantités
- **Commandes** : Passation et suivi des commandes
- **Bibliothèque personnelle** : Système de favoris pour sauvegarder les livres
- **Recherche avancée** : Recherche par titre et auteur

### 👨‍💼 Espace Administrateur
- **Gestion des livres** : Ajout, modification, suppression des livres
- **Gestion des catégories** : Organisation par genres littéraires
- **Gestion des clients** : Activation/désactivation des comptes utilisateurs
- **Suivi des commandes** : Validation et annulation des commandes
- **Tableau de bord** : Vue d'ensemble de l'activité de la librairie

## 🛠️ Technologies Utilisées

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM pour la base de données
- **Flask-Login** - Gestion de l'authentification
- **Flask-Migrate** - Gestion des migrations de base de données
- **Werkzeug** - Hachage sécurisé des mots de passe
- **SQLite** - Base de données

### Frontend
- **HTML5/CSS3** - Structure et styles
- **TailwindCSS** - Framework CSS utilitaire
- **Flowbite** - Composants UI
- **JavaScript** - Interactivité (modales, scripts)
- **Jinja2** - Moteur de templates

## 📦 Structure du Projet

```
flaskProject/
├── app.py                    # Point d'entrée principal
├── config.py                 # Configuration de l'application
├── package.json             # Dépendances frontend
├── tailwind.config.js       # Configuration TailwindCSS
├── bookstore.sqlite         # Base de données SQLite
├── migrations/              # Migrations Alembic
├── src/
│   ├── __init__.py
│   ├── admin.py            # Routes administrateur
│   ├── utilis.py           # Routes utilisateur
│   ├── models.py           # Modèles de données
│   ├── data.py             # Données de test
│   ├── fake_data.py        # Génération de données fictives
│   ├── static/
│   │   ├── css/           # Feuilles de style
│   │   ├── js/            # Scripts JavaScript
│   │   └── img/           # Images et ressources
│   └── templates/
│       ├── admin/         # Templates administrateur
│       ├── utilis/        # Templates utilisateur
│       ├── layouts/       # Templates de base
│       └── shared/        # Composants partagés
```

## 🗄️ Modèle de Données

### Tables Principales
- **User** : Utilisateurs (clients et administrateurs)
- **Livres** : Catalogue des livres
- **Categorie** : Catégories/genres des livres
- **Panier** : Paniers d'achat des utilisateurs
- **PanierItem** : Articles dans les paniers
- **Commande** : Commandes passées
- **Bibliotheque** : Favoris des utilisateurs

### Relations
- Relation many-to-many entre Livres et Catégories
- Relation one-to-many entre User et Panier/Commande/Bibliotheque
- Relation one-to-many entre Panier et PanierItem

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- Node.js (pour TailwindCSS)
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd flaskProject
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances Python**
```bash
pip install flask flask-sqlalchemy flask-login flask-migrate werkzeug
```

4. **Installer les dépendances frontend**
```bash
npm install
```

5. **Configurer la base de données**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Lancer l'application**
```bash
python app.py
```

L'application sera accessible à l'adresse : `http://localhost:5000`

## 🔧 Configuration

### Fichier `config.py`
```python
DEBUG = 1
APP_NAME = "Nuur-Library"
SQLALCHEMY_DATABASE_URI = "sqlite:///bookstore.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "votre-clé-secrète"
```

### Variables d'environnement (optionnel)
Vous pouvez définir des variables d'environnement pour une configuration plus sécurisée :
- `FLASK_ENV`
- `SECRET_KEY`
- `DATABASE_URL`

## 📱 Interface Utilisateur

### Fonctionnalités Client
- Page d'accueil avec catalogue des livres
- Page de détail pour chaque livre
- Panier d'achat interactif
- Système de recherche et filtrage
- Espace personnel avec bibliothèque de favoris
- Historique des commandes

### Fonctionnalités Administrateur
- Dashboard avec statistiques
- Interface de gestion des livres
- Gestion des utilisateurs et leurs statuts
- Suivi des commandes en temps réel

## 🔐 Système d'Authentification

- Hachage sécurisé des mots de passe avec Werkzeug
- Sessions utilisateur avec Flask-Login
- Système de rôles (USER/ADMIN)
- Protection des routes sensibles
- Gestion des statuts utilisateur (ACTIF/INACTIF)

## 📊 Base de Données

### Migrations
Le projet utilise Flask-Migrate pour la gestion des versions de la base de données :
```bash
# Créer une nouvelle migration
flask db migrate -m "Description de la migration"

# Appliquer les migrations
flask db upgrade

# Revenir à une version antérieure
flask db downgrade
```

## 🎨 Styles et Thème

- Design responsive avec TailwindCSS
- Palette de couleurs cohérente (thème marron/anti)
- Composants modulaires et réutilisables
- Interface moderne et intuitive

## 🔍 Fonctionnalités Avancées

### Recherche
- Recherche en temps réel par titre et auteur
- Suggestions de livres similaires
- Filtrage par catégories

### Gestion du Panier
- Ajout/suppression d'articles
- Modification des quantités
- Calcul automatique du total
- Persistance entre les sessions

### Système de Commandes
- Validation des commandes
- Suivi des statuts (En cours, Validé, Annulé)
- Historique complet pour les utilisateurs et administrateurs

## 🚀 Déploiement

### Déploiement local
```bash
python app.py
```

### Déploiement en production
1. Configurer les variables d'environnement
2. Utiliser un serveur WSGI (Gunicorn, uWSGI)
3. Configurer un reverse proxy (Nginx)
4. Sécuriser avec HTTPS

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Nuur Development Team**

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Contacter l'équipe de développement

---

⭐ **N'oubliez pas de donner une étoile au projet si vous l'avez trouvé utile !**
