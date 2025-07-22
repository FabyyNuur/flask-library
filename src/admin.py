
from flask import redirect, render_template, url_for,session,request
from flask_login import current_user
from datetime import datetime
from sqlalchemy import func,or_
from flask import Flask
from .utilis import app
from .models import (getAll,getLivrebyId,User, Panier,Bibliotheque, PanierItem,Commande,Categorie, Livres,db)


@app.route('/admin/bookstore')
def bookstore():
    livres = getAll()
    return render_template("admin/home.html",livres=livres,current_user=current_user)

@app.route('/admin/activ_user/<int:user_id>')
def activation(user_id):
    
    user = User.query.get(user_id)
    
    if user:
        # Changer le statut de l'utilisateur
        if user.statut == "INACTIF":
            user.statut = "ACTIF"

        
        db.session.commit()
    
    users = User.query.filter_by(role='USER').all()
    
    
    for user in users:
        # S'assurer qu'il n'y a qu'un seul panier non validé par utilisateur
        paniers_non_valides = Panier.query.filter_by(user_id=user.id, valide=False).all()
        if len(paniers_non_valides) > 1:
            # Fusionner les paniers multiples
            panier_principal = paniers_non_valides[0]
            for autre_panier in paniers_non_valides[1:]:
                for item in autre_panier.items:
                    existing_item = PanierItem.query.filter_by(panier_id=panier_principal.id, livre_id=item.livre_id).first()
                    if existing_item:
                        existing_item.nombre += item.nombre
                    else:
                        item.panier_id = panier_principal.id
                db.session.delete(autre_panier)
            db.session.commit()
            user.panier = panier_principal
        elif len(paniers_non_valides) == 1:
            user.panier = paniers_non_valides[0]
        else:
            user.panier = None
            
        user.nombre_commandes = Commande.query.filter_by(user_id=user.id).count()
        user.commandes = Commande.query.filter_by(user_id=user.id).all()
    return render_template("admin/clients.html", users=users, current_user=current_user)


@app.route('/admin/desactiv_user/<int:user_id>')
def desactivation(user_id):
    
    user = User.query.get(user_id)
    print(user)
    
    if user:
        # Changer le statut de l'utilisateur
        if user.statut == "ACTIF":
            user.statut = "INACTIF"

        
        db.session.commit()
    
    users = User.query.filter_by(role='USER').all()
    
    
    for user in users:
        # S'assurer qu'il n'y a qu'un seul panier non validé par utilisateur
        paniers_non_valides = Panier.query.filter_by(user_id=user.id, valide=False).all()
        if len(paniers_non_valides) > 1:
            # Fusionner les paniers multiples
            panier_principal = paniers_non_valides[0]
            for autre_panier in paniers_non_valides[1:]:
                for item in autre_panier.items:
                    existing_item = PanierItem.query.filter_by(panier_id=panier_principal.id, livre_id=item.livre_id).first()
                    if existing_item:
                        existing_item.nombre += item.nombre
                    else:
                        item.panier_id = panier_principal.id
                db.session.delete(autre_panier)
            db.session.commit()
            user.panier = panier_principal
        elif len(paniers_non_valides) == 1:
            user.panier = paniers_non_valides[0]
        else:
            user.panier = None
            
        user.nombre_commandes = Commande.query.filter_by(user_id=user.id).count()
        user.commandes = Commande.query.filter_by(user_id=user.id).all()
    return render_template("admin/clients.html", users=users, current_user=current_user)

@app.route('/admin/clients')
def clients():
    users = User.query.filter_by(role='USER').all()
    for user in users:
        # S'assurer qu'il n'y a qu'un seul panier non validé par utilisateur
        paniers_non_valides = Panier.query.filter_by(user_id=user.id, valide=False).all()
        if len(paniers_non_valides) > 1:
            # Fusionner les paniers multiples
            panier_principal = paniers_non_valides[0]
            for autre_panier in paniers_non_valides[1:]:
                for item in autre_panier.items:
                    existing_item = PanierItem.query.filter_by(panier_id=panier_principal.id, livre_id=item.livre_id).first()
                    if existing_item:
                        existing_item.nombre += item.nombre
                    else:
                        item.panier_id = panier_principal.id
                db.session.delete(autre_panier)
            db.session.commit()
            user.panier = panier_principal
        elif len(paniers_non_valides) == 1:
            user.panier = paniers_non_valides[0]
        else:
            user.panier = None
            
        user.nombre_commandes = Commande.query.filter_by(user_id=user.id).count()
        user.commandes = Commande.query.filter_by(user_id=user.id).all()
    return render_template("admin/clients.html", users=users, current_user=current_user)

@app.route('/admin/form-livre')
def ajout_livre():
    cate = Categorie.query.all()
    return render_template("admin/ajout.html",cate=cate)

@app.route('/admin/commandes')
def commandes_ad():
    commandes = Commande.query.all() 
    return render_template("admin/commandes.html",commandes=commandes,current_user=current_user,User=User)

@app.route("/val-commande/<int:panier_id>")
def val_commande(panier_id):
    commande = Commande.query.filter_by(panier_id=panier_id).first()
    
    if commande:
        commande.statut = "Validée"
        db.session.commit()
    
        commandes = Commande.query.all() 
        return render_template("admin/commandes.html",commandes=commandes,current_user=current_user,User=User)
    else:
        commandes = Commande.query.all() 
        return render_template("admin/commandes.html",commandes=commandes,current_user=current_user,User=User)

@app.route('/admin/ajout-livre',methods=["POST","GET"])
def ajouter_livre():
    if request.method == "POST":
        titre = request.form["title"]
        auteur = request.form["auteur"]
        description = request.form["description"]
        categories = request.form.getlist("categories[]")  # Pour récupérer plusieurs valeurs d'un champ multiple
        img_url = request.form["img_url"]
        prix = request.form["prix"]
        stock = request.form["stock"]
        volume = request.form["volume"]
        disponible = "disponible" in request.form  # Vérifie si la case à cocher est cochée
        sortie = request.form["sortie"]
        pages = request.form["pages"]
        
        # Valeurs par défaut pour les champs supprimés du formulaire
        nbre_lecteurs = 0
        nbr_etoiles = 0
        classement = 0
        
        print(titre,auteur,description)

        nouveau_livre = Livres(title=titre, auteur=auteur, description=description, img_url=img_url,
                               prix=prix, stock=stock, volume=volume, disponible=disponible, sortie=sortie,
                               nbre_lecteurs=nbre_lecteurs, nbr_etoiles=nbr_etoiles, classement=classement, pages=pages)
        print(nouveau_livre)
        # Ajouter les catégories au livre
        for categorie_id in categories:
            categorie = Categorie.query.get(categorie_id)
            if categorie:
                nouveau_livre.categories.append(categorie)

        # Enregistrer le nouveau livre dans la base de données
        db.session.add(nouveau_livre)
        db.session.commit()

        livres = getAll()
        return render_template("admin/home.html",livres=livres,current_user=current_user)

    # Gérer le cas où la méthode n'est pas POST
    cate = Categorie.query.all()
    return render_template("admin/ajout.html",cate=cate)