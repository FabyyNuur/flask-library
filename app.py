from src import app
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from src.models import User,db,Livres
from flask import render_template,session,request, redirect,Flask
from flask_login import (
                            LoginManager,
                            UserMixin,
                            login_user,
                            login_required,
                            current_user,
                            logout_user
                        )
app.config.from_pyfile("../config.py")

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
        
        # Créer un nouvel utilisateur
        new_user = User(username=username, password=generate_password_hash(password), statut='ACTIF', role='USER')
        db.session.add(new_user)
        db.session.commit()
    
    return render_template("layouts/login.html")

@app.route('/compte')
def compte():
    return render_template("layouts/compte.html")

@app.route('/')
@login_required  
def home1():
    # Rediriger vers la page appropriée selon le rôle de l'utilisateur
    if current_user.role == 'USER':
        return redirect("/shop")
    else:
        return redirect("/admin/bookstore")

@app.route("/home")
@login_required
def home():
    return render_template("layouts/base.html",current_user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    return render_template("layouts/login.html")


if __name__ == '__main__':
    # session.pop('panier_id', None)
    app.run(debug=True, port=5001)
