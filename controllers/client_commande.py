#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT id_gant, nom_gant AS nom, prix_gant AS prix, quantite
    FROM gant
    JOIN ligne_panier ON gant.id_gant = ligne_panier.gant_id
    WHERE ligne_panier.utilisateur_id=%s;
    '''
    mycursor.execute(sql, (id_client,))
    gants_panier = mycursor.fetchall()
    if len(gants_panier) >= 1:
        sql = '''SELECT SUM(prix_gant*quantite) AS prix_total
        FROM gant
        JOIN ligne_panier on gant.id_gant=ligne_panier.gant_id
        WHERE ligne_panier.utilisateur_id=%s'''
        mycursor.execute(sql, (id_client,))
        prix_total = mycursor.fetchone()["prix_total"]
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , gants_panier=gants_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = '''SELECT *, quantite*prix_gant AS prix
    FROM ligne_panier
    JOIN gant ON ligne_panier.gant_id=gant.id_gant
    WHERE utilisateur_id=%s'''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas de gants dans le ligne_panier', 'alert-warning')
        return redirect('/client/gant/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    a = datetime.now()

    sql = '''INSERT INTO commande (date_achat, etat_id, utilisateur_id)
    VALUES (%s, 1, %s)'''
    mycursor.execute(sql, (a,id_client))
    get_db().commit()

    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    id_commande = mycursor.fetchone()['last_insert_id']
    # numéro de la dernière commande
    for item in items_ligne_panier:
        print(item)
        sql = '''DELETE FROM ligne_panier
        WHERE ligne_panier.gant_id=%s AND ligne_panier.utilisateur_id = %s'''
        mycursor.execute(sql, (item["gant_id"], item["utilisateur_id"]))
        get_db().commit()
        sql = '''INSERT INTO ligne_commande (commande_id, gant_id, quantite, prix)
        VALUES (%s, %s, %s, %s)
        '''
        mycursor.execute(sql, (id_commande, item["gant_id"], item["quantite"], item["prix"]))
        get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/gant/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
     SELECT commande.etat_id,
    utilisateur.login,
    SUM(ligne_commande.quantite) as nbr_gants,
    SUM(ligne_commande.prix * ligne_commande.quantite) as prix_total,
    commande.date_achat,
    etat.libelle_etat as libelle,
    commande.id_commande
     FROM commande
     JOIN utilisateur on utilisateur.id_utilisateur = commande.utilisateur_id
     JOIN ligne_commande on ligne_commande.commande_id = commande.id_commande
     JOIN etat on etat.id_etat = commande.etat_id
     WHERE commande.utilisateur_id=%s
     GROUP BY commande.id_commande
     ORDER BY etat_id, date_achat DESC;'''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()
    gants_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        sql = '''SELECT gant.nom_gant as nom,
        ligne_commande.quantite,
        ligne_commande.prix,
        (ligne_commande.quantite * ligne_commande.prix) as prix_ligne,
        commande.etat_id,
        commande.id_commande AS id
        FROM ligne_commande
        JOIN gant ON ligne_commande.gant_id = gant.id_gant
        JOIN commande on commande.id_commande = ligne_commande.commande_id
        WHERE ligne_commande.commande_id = %s AND commande.utilisateur_id=%s;'''
        mycursor.execute(sql, (id_commande,id_client))
        gants_commande = mycursor.fetchall()

        if gants_commande==():
            flash("Cette commande ne vous appartient pas", "alert-warning")

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , gants_commande=gants_commande
                           , commande_adresses=commande_adresses
                           )

