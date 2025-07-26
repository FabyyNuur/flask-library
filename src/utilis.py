# pylint: disable=astroid-error
from flask import redirect, render_template, url_for,session,request
from flask_login import current_user
from datetime import datetime
from sqlalchemy import func,or_
from flask import jsonify

# Importer l'app et db depuis __init__.py
from . import app, db

from .models import (getAll,getLivrebyId,User, Panier,Bibliotheque, PanierItem,Commande,Categorie, Livres,db)
from flask_login import login_required, current_user

@app.route('/shop')
@login_required
def home_user():
    livres = getAll()
    return render_template("utilis/home.html",livres=livres,current_user=current_user)

@app.route("/livres/<int:id_livre>")
def detail_livre_c(id_livre):
    prod = getLivrebyId(id_livre)
    if not prod:
        return redirect(url_for("home_user"))

    categories = [categorie.id for categorie in prod.categories]

    # Rechercher tous les livres qui ont au moins une catégorie en commun avec le livre spécifié, à l'exception du livre spécifié
    livres_similaires = Livres.query.filter(Livres.id != id_livre, Livres.categories.any(Categorie.id.in_(categories))).all()

    return render_template("utilis/livre.html", livre=prod, livres_similaires=livres_similaires)

@app.route("/sup-panier/<int:id_livre>")
@login_required
def sup_du_panier(id_livre):
    """Supprime un livre du panier"""
    try:
        if 'panier_id' not in session:
            return redirect(url_for('panier', user_id=current_user.id))
            
        panier = Panier.query.get(session['panier_id'])
        if not panier or panier.user_id != current_user.id:
            return redirect(url_for('panier', user_id=current_user.id))
        
        item_a_supprimer = PanierItem.query.filter_by(panier_id=panier.id, livre_id=id_livre).first()
        
        if item_a_supprimer:
            db.session.delete(item_a_supprimer)
            db.session.commit()
        
        return redirect(url_for('panier', user_id=current_user.id))
    except Exception as e:
        print(f"Erreur suppression panier: {e}")
        return redirect(url_for('panier', user_id=current_user.id))
    
    
@app.route("/sup-commande/<int:panier_id>")
def sup_commande(panier_id):
    commande = Commande.query.filter_by(panier_id=panier_id).first()
    
    if commande:
        # Supprimer la commande
        db.session.delete(commande)
        db.session.commit()
    
        return redirect(url_for('commandes', user_id=current_user.id))
    else:
        return redirect(url_for('commandes', user_id=current_user.id))

@app.route('/ajoutPanier/<int:livre_id>')
@login_required
def ajoutPanier(livre_id):
    """Ajoute un livre au panier de l'utilisateur"""
    try:
        print(f"Tentative d'ajout du livre {livre_id} au panier pour l'utilisateur {current_user.id}")
        session.pop('commande_id', None)
        
        # Chercher un panier non validé existant pour cet utilisateur
        panier = Panier.query.filter_by(user_id=current_user.id, valide=False).first()
        
        if not panier:
            # Créer un nouveau panier seulement s'il n'y en a aucun non validé
            panier = Panier(user_id=current_user.id, valide=False)
            db.session.add(panier)
            db.session.flush()  # Pour obtenir l'ID sans commit complet
            session['panier_id'] = panier.id
            print(f"Nouveau panier créé avec l'ID: {panier.id}")
        else:
            session['panier_id'] = panier.id
            print(f"Utilisation du panier existant: {panier.id}")
            
            # S'assurer qu'il n'y a qu'un seul panier non validé (nettoyage)
            autres_paniers = Panier.query.filter_by(user_id=current_user.id, valide=False).filter(Panier.id != panier.id).all()
            if autres_paniers:
                print(f"Suppression de {len(autres_paniers)} paniers en double")
                for autre_panier in autres_paniers:
                    # Transférer les articles vers le panier principal
                    for item in autre_panier.items:
                        existing_item = PanierItem.query.filter_by(panier_id=panier.id, livre_id=item.livre_id).first()
                        if existing_item:
                            existing_item.nombre += item.nombre
                        else:
                            item.panier_id = panier.id
                    db.session.delete(autre_panier)
        
        # Vérifier si le livre existe déjà dans le panier
        existing_item = PanierItem.query.filter_by(panier_id=panier.id, livre_id=livre_id).first()
        if existing_item:
            existing_item.nombre += 1
            print(f"Quantité mise à jour pour le livre {livre_id}: {existing_item.nombre}")
        else:
            # Vérifier que le livre existe
            livre = Livres.query.get(livre_id)
            if not livre:
                print(f"Livre {livre_id} non trouvé")
                return redirect(url_for('home_user'))
            
            new_item = PanierItem(panier_id=panier.id, livre_id=livre_id, nombre=1)
            db.session.add(new_item)
            print(f"Nouvel article ajouté: livre {livre_id} ('{livre.title}') dans panier {panier.id}")
        
        # Calculer le total du panier
        panier.total = sum(item.livre.prix * item.nombre for item in panier.items if item.livre)
        
        db.session.commit()
        print("Changements sauvegardés en base de données")
        print(f"Panier {panier.id} contient maintenant {len(panier.items)} articles")
        
        return redirect(url_for('panier', user_id=current_user.id))
    except Exception as e:
        print(f"Erreur ajout panier: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return redirect(url_for('home_user'))

@app.route('/ajout-commande/<int:panier_id>')
def ajoutCommande(panier_id):
    if 'commande_id' not in session:
        panier = Panier.query.get(panier_id)
        session.pop('panier_id', None)
        # print(panier.items)
        if panier is None or panier.valide:  # Ensure panier exists and is not already validated
            return redirect(url_for('panier', user_id=current_user.id))

        total = sum(item.livre.prix * item.nombre for item in panier.items)
        commande = Commande(user_id=current_user.id, panier_id=panier_id, date_commande=datetime.now().date(), total=total, statut="En Cours")
        print(commande)
        db.session.add(commande)
        db.session.commit()
        session['commande_id'] = commande.id

        panier.valide = True
        session.pop('panier_id', None)
        session.pop('commande_id', None)
        db.session.commit()
    else:
        commande = Commande.query.get(session['commande_id'])

    return redirect(url_for('commandes', user_id=current_user.id))

@app.route('/panier/<int:user_id>')
def panier(user_id):
    print(f"Affichage du panier pour l'utilisateur {user_id}")
    # S'assurer qu'il n'y a qu'un seul panier non validé
    paniers_non_valides = Panier.query.filter_by(user_id=user_id, valide=False).all()
    
    if len(paniers_non_valides) > 1:
        # Fusionner tous les paniers non validés en un seul
        print(f"Fusion de {len(paniers_non_valides)} paniers non validés")
        panier_principal = paniers_non_valides[0]  # Garder le premier
        
        for i, autre_panier in enumerate(paniers_non_valides[1:], 1):
            print(f"Fusion du panier {autre_panier.id} dans le panier {panier_principal.id}")
            # Transférer tous les articles
            for item in autre_panier.items:
                existing_item = PanierItem.query.filter_by(panier_id=panier_principal.id, livre_id=item.livre_id).first()
                if existing_item:
                    existing_item.nombre += item.nombre
                else:
                    item.panier_id = panier_principal.id
            
            # Supprimer l'ancien panier
            db.session.delete(autre_panier)
        
        db.session.commit()
        panier = panier_principal
    elif len(paniers_non_valides) == 1:
        panier = paniers_non_valides[0]
    else:
        panier = None
    
    if panier:
        print(f"Panier trouvé: ID {panier.id}, {len(panier.items)} articles")
        # Calculer le total en s'assurant que tous les livres existent
        total = 0
        for item in panier.items:
            if item.livre:
                total += item.livre.prix * item.nombre
                print(f"Article: {item.livre.title}, Quantité: {item.nombre}, Prix: {item.livre.prix}")
            else:
                print(f"Article avec livre_id {item.livre_id} manquant")
        
        panier.total = total
        db.session.commit()
        
        return render_template('utilis/panier.html', items=panier.items, total=panier.total, id=panier.id)
    else:
        print("Aucun panier non validé trouvé")
    
    return render_template("layouts/vide.html", name="PANIER")
    # panier_id = session.get('panier_id')
    # if panier_id:
    #     panier = Panier.query.get(panier_id)
    #     # panier = Panier.query.filter(Panier.id == panier_id, Panier.valide == False).first()
    #     print(panier.valide)
    
        # if panier.valide == False:
        #     if panier.user_id != user_id:
        #         return render_template("layouts/vide.html",name="PANIER")
        #     panier.total = sum(item.livre.prix * item.nombre for item in panier.items)
        #     db.session.commit()
        # total = sum(item.livre.prix * item.nombre for item in items)
        # mettre_a_jour_total_panier(session['panier_id'])
            # return render_template('utilis/panier.html', items=panier.items,total=panier.total,id=panier.id)
    # return render_template("layouts/vide.html",name="PANIER")

@app.route('/commande/<int:user_id>')
def commandes(user_id):
    commandes = Commande.query.join(Panier).filter(Panier.user_id == user_id).all()
    if commandes:
        return render_template('utilis/commande.html', commandes=commandes,user=User.query.get(user_id))
    else:
        return render_template("layouts/vide.html", name="COMMANDES")

@app.route('/search', methods=["POST","GET"])
@login_required
def research():
    if request.method == "POST":
        # Récupérer le terme de recherche depuis le formulaire
        mot = request.form.get("recherche", "").strip()
        print(f"Recherche pour: {mot}")
        
        if not mot:  # Si aucun terme de recherche
            livres_trouves = getAll()
        else:
            # Rechercher les livres dont le titre ou l'auteur contient le mot spécifié
            livres_trouves = Livres.query.filter(
                or_(
                    Livres.title.ilike(f"%{mot}%"), 
                    Livres.auteur.ilike(f"%{mot}%")
                )
            ).all()
            print(f"Livres trouvés: {len(livres_trouves)}")
    else:
        # GET request - afficher tous les livres
        livres_trouves = getAll()
        
    # Rediriger selon le rôle de l'utilisateur
    if current_user.role == "USER":
        return render_template("utilis/home.html", livres=livres_trouves, current_user=current_user)
    else:
        return render_template("admin/home.html", livres=livres_trouves, current_user=current_user)
    

@app.route('/ajout-fav/<int:livre_id>')
@login_required
def ajoutBiblio(livre_id):
    """Ajoute un livre aux favoris (bibliothèque)"""
    try:
        bibliotheque = Bibliotheque.query.filter_by(user_id=current_user.id).first()
        if bibliotheque is None:
            bibliotheque = Bibliotheque(user_id=current_user.id)
            db.session.add(bibliotheque)
            db.session.commit()

        livre = Livres.query.get(livre_id)
        if livre is not None:
            # Vérifier si le livre est déjà dans la bibliothèque
            if livre not in bibliotheque.livres:
                bibliotheque.livres.append(livre)
                db.session.commit()
            
        return redirect(url_for('bibliotheque'))
    except Exception as e:
        print(f"Erreur ajout favori: {e}")
        return redirect(url_for('home_user'))

@app.route('/sup-fav/<int:livre_id>')
@login_required
def sup_livre_biblio(livre_id):
    """Supprime un livre des favoris (bibliothèque)"""
    try:
        bibliotheque = Bibliotheque.query.filter_by(user_id=current_user.id).first()
        if not bibliotheque:
            return redirect(url_for('bibliotheque'))

        livre = Livres.query.get(livre_id)
        if livre and livre in bibliotheque.livres:
            bibliotheque.livres.remove(livre)
            db.session.commit()
        
        return redirect(url_for('bibliotheque'))
    except Exception as e:
        print(f"Erreur suppression favori: {e}")
        return redirect(url_for('bibliotheque'))
        if livre in bibliotheque.livres:
            bibliotheque.livres.remove(livre)
            db.session.commit()
            return render_template("utilis/bibliotheque.html", livres=bibliotheque.livres, current_user=current_user)
            
        else:
            return render_template("utilis/bibliotheque.html", livres=bibliotheque.livres, current_user=current_user)

    else:
        return render_template("utilis/bibliotheque.html", livres=bibliotheque.livres, current_user=current_user)


@app.route('/bibliotheque')
@login_required
def bibliotheque():
    """Affiche la bibliothèque personnelle de l'utilisateur (favoris)"""
    try:
        user_id = current_user.id
        bibliotheque = Bibliotheque.query.filter_by(user_id=user_id).first()
        
        if bibliotheque:
            livres = bibliotheque.livres
        else:
            # Créer une bibliothèque vide si elle n'existe pas
            bibliotheque = Bibliotheque(user_id=user_id)
            db.session.add(bibliotheque)
            db.session.commit()
            livres = []
        
        return render_template("utilis/bibliotheque.html", livres=livres, current_user=current_user)
    except Exception as e:
        print(f"Erreur dans bibliothèque: {e}")
        return render_template("utilis/bibliotheque.html", livres=[], current_user=current_user)