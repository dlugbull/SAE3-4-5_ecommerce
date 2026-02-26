#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


""""@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_gant = request.form.get('id_gant')
    quantite = request.form.get('quantite')

    # ---------

    id_declinaison_gant=request.form.get('id_declinaison_gant',None)
    id_declinaison_gant = 1

# ajout dans le panier d'une déclinaison d'un gant (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_gant))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_gant = declinaisons[0]['id_declinaison_gant']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_gant))
    #     gant = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_gant.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , gant=gant)

# ajout dans le panier d'un gant"""

@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_gant = request.form.get('id_gant')
    quantite = request.form.get('quantite')
    """id_taille = request.form.get('id_taille', None)
    id_taille = 1"""

    sql = "SELECT * FROM ligne_panier WHERE gant_id = %s AND utilisateur_id = %s"
    mycursor.execute(sql, (id_gant, id_client))
    gant_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM gant WHERE id_gant = %s", (id_gant,))
    gant = mycursor.fetchone()

    if not (gant_panier is None) and gant_panier['quantite'] >= 1:
        tuple_update = (quantite, id_client, id_gant)
        sql = "UPDATE ligne_panier SET quantite = quantite + %s WHERE utilisateur_id = %s AND gant_id = %s"
        mycursor.execute(sql, tuple_update)
    else:
        sql = "INSERT INTO ligne_panier(utilisateur_id, gant_id, quantite, date_ajout) VALUES (%s, %s, %s, current_timestamp)"
        tuple_insert = (id_client, id_gant, quantite)
        mycursor.execute(sql, tuple_insert)

    get_db().commit()
    return redirect('/client/gant/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_gant = request.form.get('id_gant','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'gant
    # id_declinaison_gant = request.form.get('id_declinaison_gant', None)

    sql = ''' selection de la ligne du panier pour l'gant et l'utilisateur connecté'''
    gant_panier=[]

    if not(gant_panier is None) and gant_panier['quantite'] > 1:
        sql = ''' mise à jour de la quantité dans le panier => -1 gant '''
    else:
        sql = ''' suppression de la ligne de panier'''

    # mise à jour du stock de l'gant disponible
    get_db().commit()
    return redirect('/client/gant/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' sélection des lignes de panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de le gant pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de le gant : stock = stock + qté de la ligne pour le gant'''
        get_db().commit()
    return redirect('/client/gant/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_gant = request.form.get('id_declinaison_gant')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de le gant : stock = stock + qté de la ligne pour le gant'''

    get_db().commit()
    return redirect('/client/gant/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    if filter_word != None or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash("Le mot recherché ne doit etre composé que de lettres !")
        else:
            if len(filter_word) == 1:
                flash("le mot recherché doit contenir au moins 2 lettres !")
            else:
                session.pop('filter_word', None)
    if filter_prix_max or filter_prix_min:
        filter_prix_min = str(filter_prix_min).replace(' ', '').replace(',', '.')
        filter_prix_max = str(filter_prix_max).replace(' ', '').replace(',', '.')
        if filter_prix_min.replace('.', '', 1).isdigit() and filter_prix_max.replace('.', '', 1).isdigit():
            if float(filter_prix_max) > float(filter_prix_min):
                session['filter_prix_max'] = filter_prix_max
                session['filter_prix_min'] = filter_prix_min
            else:
                flash("le maximum doit être supérieur au minimum")
        else:
            flash("min et max doivent être des numériques")
    else:
        session.pop('filter_prix_max', None)
        session.pop('filter_prix_min', None)
    filter_types = [t for t in filter_types if t != '']
    if filter_types:
        session['filter_types'] = filter_types
    else:
        session.pop('filter_types', None)
    return redirect('/client/gant/show')

@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    return redirect('/client/gant/show')
