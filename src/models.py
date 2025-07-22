# pylint: disable=astroid-error
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate # type: ignore
from .utilis import app

from flask_login import (UserMixin)


db = SQLAlchemy(app)
migrate = Migrate(app,db)

livres_categories = db.Table('livres_categories',
    db.Column('livre_id', db.Integer, db.ForeignKey('livres.id'), primary_key=True),
    db.Column('categorie_id', db.Integer, db.ForeignKey('categorie.id'), primary_key=True)
)

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), unique=True)
    livres = db.relationship('Livres',
                             secondary=livres_categories,
                             back_populates='categories',
                             primaryjoin="Categorie.id==livres_categories.c.categorie_id")
    
class Livres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    auteur = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    categories = db.relationship('Categorie',
                                 secondary=livres_categories,
                                 back_populates='livres',
                                 primaryjoin="Livres.id==livres_categories.c.livre_id")
    img_url = db.Column(db.Text)
    prix = db.Column(db.Integer)
    stock = db.Column(db.Integer, default=0)
    volume = db.Column(db.Integer)
    disponible = db.Column(db.Boolean,default=True)
    sortie = db.Column(db.Text)
    nbre_lecteurs = db.Column(db.Integer)
    nbr_etoiles = db.Column(db.Integer)
    classement= db.Column(db.Integer)
    pages=db.Column(db.Integer)

   # maison edition

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(250))
    role = db.Column(db.String(50), default='USER')
    statut = db.Column(db.String(50), default='ACTIF')
    paniers = db.relationship('Panier', backref='user', lazy=True)
    commandes = db.relationship('Commande', backref='user', lazy=True)
    
class Panier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('PanierItem', back_populates='panier')
    total = db.Column(db.Float, default=0.0)
    valide = db.Column(db.Boolean, default=False)

class PanierItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    panier_id = db.Column(db.Integer, db.ForeignKey('panier.id'))
    livre_id = db.Column(db.Integer, db.ForeignKey('livres.id'))
    nombre = db.Column(db.Integer, default=1)
    panier = db.relationship('Panier', back_populates='items')
    livre = db.relationship('Livres')
    
class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    panier_id = db.Column(db.Integer, db.ForeignKey('panier.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_commande = db.Column(db.DateTime, default=db.func.current_timestamp())
    statut = db.Column(db.String(100), default='En cours')
    total = db.Column(db.Float)
    panier = db.relationship('Panier', backref=db.backref('commande', uselist=False))

class Bibliotheque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='bibliotheques')
    livres = db.relationship('Livres', secondary='bibliotheque_livres', backref='bibliotheques')

bibliotheque_livres = db.Table('bibliotheque_livres',
    db.Column('bibliotheque_id', db.Integer, db.ForeignKey('bibliotheque.id')),
    db.Column('livre_id', db.Integer, db.ForeignKey('livres.id'))
)


with app.app_context():
    # db.drop_all()
    db.create_all()
    
def getAll():
    # Temporaire: retourner tous les livres pour le debug
    all_books = Livres.query.options(db.joinedload(Livres.categories)).all()
    print(f"DEBUG: Nombre total de livres: {len(all_books)}")
    for book in all_books:
        print(f"DEBUG: Livre {book.id}: {book.title}, disponible: {book.disponible}")
    return all_books
    # return Livres.query.filter(Livres.disponible == True).options(db.joinedload(Livres.categories)).all()

def getLivrebyId(id_livre):
    # return "SELECT * FROM product where id = is_livre"
    return Livres.query.get(id_livre)

def saveLivres(l: Livres):
    db.session.add(l)
    db.session.commit()


    

# hashed_password = generate_password_hash('passer')
# new_user = User(username='pasall', password=hashed_password)
# db.session.add(new_user)
# hashed_password = generate_password_hash('nuur2003')
# new_user = User(username='nuura', password=hashed_password)
# db.session.add(new_user)
# hashed_password = generate_password_hash('abiba')
# new_user = Categorie(libelle='Smut')
# db.session.add(new_user)
# db.session.commit()