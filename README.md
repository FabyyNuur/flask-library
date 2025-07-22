# 📚 Nuur-Library - Système de Gestion de Librairie en Ligne

Application web moderne développée avec Flask pour gérer une librairie en ligne, offrant une expérience complète pour les clients et les administrateurs.

---

## Fonctionnalités principales

### Espace Client

- Authentification sécurisée (connexion/déconnexion)
- Navigation et recherche dans le catalogue de livres
- Détail complet des livres (auteur, catégories, prix, description…)
- Panier d'achat interactif
- Passation et suivi des commandes
- Bibliothèque personnelle (favoris)
- Recherche avancée (titre, auteur)

### Espace Administrateur

- Gestion des livres (ajout, suppression)
- Gestion des catégories
- Gestion des clients (activation/désactivation)
- Suivi des commandes
- Tableau de bord synthétique

---

## 🛠️ Technologies

- **Backend** : Flask, SQLAlchemy, Flask-Login, Flask-Migrate, Werkzeug, SQLite
- **Frontend** : HTML5, CSS3, TailwindCSS, Flowbite, JavaScript, Jinja2

---

## 📦 Structure du projet

```
flaskProject/
├── app.py
├── config.py
├── package.json
├── tailwind.config.js
├── bookstore.sqlite
├── migrations/
├── src/
│   ├── admin.py
│   ├── utilis.py
│   ├── models.py
│   ├── data.py
│   ├── fake_data.py
│   ├── static/
│   └── templates/
```

---

## Modèle de données

- **User** : Utilisateurs (clients/admins)
- **Livres** : Catalogue
- **Categorie** : Genres
- **Panier** : Paniers d'achat
- **PanierItem** : Articles du panier
- **Commande** : Commandes passées
- **Bibliotheque** : Favoris

---

## Installation rapide

1. Cloner le repo et se placer dans le dossier
2. Créer un environnement virtuel et activer
3. Installer les dépendances Python et Node.js
4. Initialiser la base de données (`flask db upgrade`)
5. Lancer l'application : `python app.py`

---

## Authentification & sécurité

- Hachage des mots de passe (Werkzeug)
- Sessions sécurisées (Flask-Login)
- Système de rôles (USER/ADMIN)
- Protection des routes sensibles

---

## UI & Expérience

- Design responsive (TailwindCSS)
- Composants réutilisables
- Interface moderne et intuitive

---

## Corrections & évolutions futures

### Corrections récentes

- Correction de la gestion des paniers multiples (fusion automatique)
- Refonte du design admin (cartes, grilles, responsive)
- Sécurisation des routes et des statuts utilisateurs

### Évolutions prévues

- **Création de compte** : permettre l'inscription directe des utilisateurs
- **Gestion avancée des catégories** : ajout, modification, suppression depuis l'admin
- **Gestion des auteurs** : lier chaque livre à un ou plusieurs auteurs, CRUD auteurs
- **Modification des livres** : permettre l'édition complète des informations d'un livre
- **Ajout du champ ISBN** : stocker et afficher l'ISBN pour chaque livre
- **Gestion des stocks** : suivi des quantités disponibles
- **Notifications** : alertes pour commandes, ruptures de stock, etc.
- **Statistiques avancées** : ventes, livres populaires, activité utilisateur
- **Amélioration de la recherche** : filtres combinés, suggestions dynamiques
- **Autres fonctionnalités manquantes** : gestion des retours, wishlist, etc.

---

## Contribution

Contributions bienvenues ! Fork, branche, PR.

---

## Support

uicode.byfatoubintg@gmail.com

⭐ **Merci d'utiliser Nuur-Library !**

---
