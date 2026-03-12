#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_gant = Blueprint('client_gant', __name__,
                        template_folder='templates')

@client_gant.route('/client/index')
@client_gant.route('/client/gant/show')              # remplace /client
def client_gant_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
          SELECT gant.id_gant
               , gant.nom_gant AS nom
               , gant.poids AS poids
               , gant.couleur AS couleur
               , gant.prix_gant AS prix
               , gant.photo AS photo
               , gant.fournisseur AS fournisseur
               , gant.marque AS marque
               , gant.type_gant_id AS type
               , sum(declinaison_gant.stock) AS stock
          FROM gant
              JOIN declinaison_gant ON gant.id_gant = declinaison_gant.gant_id
          WHERE id_gant IS NOT NULL \
          '''

    # utilisation du filtre
    list_param = []
    if session.get('filter_word', None):
        sql += " AND gant.nom_gant LIKE %s "
        filter_word = session['filter_word']
        list_param.append('%' + filter_word + '%')
    if session.get('filter_prix_min', None):
        list_param.append(session['filter_prix_min'])
        sql += " AND gant.prix_gant >= %s"
    if session.get('filter_prix_max', None):
        list_param.append(session['filter_prix_max'])
        sql += " AND gant.prix_gant <= %s"
    if session.get('filter_types', None):
        liste_types = [t for t in session['filter_types'] if t != '']
        if liste_types:
            sql += " AND ( "
            for i in range(len(liste_types)):
                sql += "gant.type_gant_id = %s"
                list_param.append(liste_types[i])
                if i < len(liste_types) - 1:
                    sql += " OR "
            sql += ")"


    sql += '''GROUP BY id_gant 
        ORDER BY nom_gant'''
    # print("SQL:", sql)
    mycursor.execute(sql, tuple(list_param))
    gants = mycursor.fetchall()
    # print("Nombre de gants:", len(gants))

    # print("Params:", list_param)

    # pour le filtre
    sql = '''SELECT type_gant.id_type_gant,
                    type_gant.nom_type_gant as nom FROM type_gant'''
    mycursor.execute(sql)
    types_gant = mycursor.fetchall()

    sql='''SELECT ligne_panier.utilisateur_id,
                  ligne_panier.declinaison_gant_id as id_gant,
                  ligne_panier.quantite,
                  ligne_panier.date_ajout,
                  gant.prix_gant as prix,
                  gant.nom_gant as nom,
                  sum(declinaison_gant.stock) AS stock
           FROM ligne_panier
                    JOIN declinaison_gant
                        ON ligne_panier.declinaison_gant_id = declinaison_gant.id_declinaison_gant
                    JOIN gant
                        ON declinaison_gant.gant_id = gant.id_gant
           WHERE ligne_panier.utilisateur_id=%s
           GROUP BY declinaison_gant_id'''

    mycursor.execute(sql,(id_client,))
    gants_panier = mycursor.fetchall()
    print(gants_panier)

    if len(gants_panier) >= 1:
        sql = ''' SELECT sum(declinaison_gant.prix_declinaison * ligne_panier.quantite) AS prix
                  FROM declinaison_gant
                           JOIN ligne_panier ON ligne_panier.declinaison_gant_id = declinaison_gant.id_declinaison_gant
                  WHERE utilisateur_id = %s'''
        mycursor.execute(sql, (id_client,))
        prix_total = mycursor.fetchone()["prix"]
    else:
        prix_total = 0
    mycursor.close()
    return render_template('client/boutique/panier_gant.html'
                           , gants=gants
                           , gants_panier=gants_panier
                           , prix_total=prix_total
                           , items_filtre=types_gant
                           )
