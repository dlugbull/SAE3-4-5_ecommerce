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

    sql = '''   selection des gants   '''
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    gants =[]


    # pour le filtre
    types_gant = []


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
