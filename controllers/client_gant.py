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
       WHERE stock > 0
       ORDER BY nom_gant
       '''
    mycursor.execute(sql)
    gants = mycursor.fetchall()
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3='''
    SELECT id_type_gant AS id
       , nom_type_gant AS libelle
       FROM type_gant
       ORDER BY nom_type_gant
       '''
    mycursor.execute(sql3)
    types_gant = mycursor.fetchall()


    gants_panier = []

    if len(gants_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_gant.html'
                           , gants=gants
                           , gants_panier=gants_panier
                           #, prix_total=prix_total
                           , items_filtre=types_gant
                           )
