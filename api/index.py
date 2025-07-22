import sys
import os

# Ajouter le répertoire parent au path pour pouvoir importer les modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import app
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import User, db, Livres
from flask import render_template, session, request, redirect
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, 
    current_user, logout_user
)

# Configuration pour la production
app.config.update({
    'DEBUG': False,
    'TESTING': False,
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'NurulHalbiii'),
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL', 'sqlite:///bookstore.sqlite'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'USE_SESSION_FOR_NEXT': True
})

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Connecter vous pour acceder a cette page!!!😜"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return render_template("layouts/login.html")

        if user and user.statut == 'ACTIF' and check_password_hash(user.password, password):
            login_user(user)
            if current_user.role == 'USER':
                return redirect("/shop")
            else:
                return redirect("/admin/bookstore")
        else:
            return render_template("layouts/login.html")
    
    return render_template("layouts/login.html")

@app.route('/creer-compte', methods=["GET", "POST"])
def creer_compte():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("layouts/compte.html", error="Cet utilisateur existe déjà")
        
        # Créer un nouvel utilisateur
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        except Exception as e:
            db.session.rollback()
            return render_template("layouts/compte.html", error="Erreur lors de la création du compte")
    
    return render_template("layouts/compte.html")

@app.route("/")
def home():
    return render_template("layouts/base.html", current_user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    return render_template("layouts/login.html")

# Cette fonction est appelée par Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

# Pour le développement local et les tests
if __name__ == '__main__':
    app.run(debug=False)

# Export pour Vercel
app = app
