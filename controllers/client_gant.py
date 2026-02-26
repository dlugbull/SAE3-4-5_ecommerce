#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_gant = Blueprint('client_gant', __name__,
                        template_folder='templates')

@client_gant.route('/client/index')
@client_gant.route('/client/gant/show')              # remplace /client@client_gant.route('/client/index')
def client_gant_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Construction dynamique du filtre
    conditions = ["stock > 0"]

    if session.get('filter_word'):
        conditions.append(f"nom_gant LIKE %{session['filter_word']}%")

    if session.get('filter_prix_min') and session.get('filter_prix_max'):
        conditions.append(f"prix_gant BETWEEN {session['filter_prix_min']} AND {session['filter_prix_max']}")

    if session.get('filter_types'):
        placeholders=[]
        for type_id in session['filter_types']:
            placeholders.append(f"type_gant_id = {type_id}")
        conditions.append(" OR ".join(placeholders))

    where_clause = " AND ".join(conditions)
    print(where_clause)

    sql = f'''
       SELECT id_gant AS id
       , nom_gant AS nom
       , poids AS poids
       , couleur AS couleur
       , prix_gant AS prix
       , photo AS photo
       , fournisseur AS fournisseur
       , marque AS marque
       , type_gant_id AS type
       , stock AS stock
       , taille_id AS taille
       FROM gant
       WHERE {where_clause}
       ORDER BY nom_gant
       '''
    mycursor.execute(sql)
    gants = mycursor.fetchall()
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3='''
    SELECT id_type_gant
       , nom_type_gant AS libelle
       FROM type_gant
       ORDER BY nom_type_gant
       '''
    mycursor.execute(sql3)
    types_gant = mycursor.fetchall()

    sql4='''
    SELECT gant_id, quantite, date_ajout, prix_gant as prix, nom_gant as nom
    FROM ligne_panier
    JOIN gant ON ligne_panier.gant_id = gant.id_gant
    WHERE utilisateur_id = %s;
    '''
    mycursor.execute(sql4, (id_client))
    gants_panier = mycursor.fetchall()
    print(gants_panier)

    if len(gants_panier) >= 1:
        sql = ''' SELECT sum(gant.prix_gant * ligne_panier.quantite) AS prix
         FROM gant
         JOIN ligne_panier ON ligne_panier.gant_id = gant.id_gant
         WHERE utilisateur_id = %s'''
        mycursor.execute(sql, (id_client))
        prix_total = mycursor.fetchone()["prix"]
    else:
        prix_total = 0
    return render_template('client/boutique/panier_gant.html'
                           , gants=gants
                           , gants_panier=gants_panier
                           , prix_total=prix_total
                           , items_filtre=types_gant
                           )
