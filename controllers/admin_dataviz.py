#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                          template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_gant_stock():
    mycursor = get_db().cursor()
    sql = '''SELECT type_gant.nom_type_gant as libelle, type_gant.id_type_gant,
                    count(gant.type_gant_id) as nbr_gants
             FROM type_gant
                      JOIN gant ON type_gant.id_type_gant = gant.type_gant_id
             GROUP BY type_gant.nom_type_gant, type_gant.id_type_gant \
           '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['libelle']) for row in datas_show]
    values = [int(row['nbr_gants']) for row in datas_show]

    mycursor.execute(sql)
    types_gants_nb = mycursor.fetchall()

    mycursor.close()
    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values
                           , types_gants_nb=types_gants_nb)





@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_adresses():
    mycursor = get_db().cursor()

    sql = """
        SELECT
            LEFT(a.code_postal, 2) AS dep,
            COUNT(DISTINCT c.id_commande) AS nb_ventes,
            SUM(lc.quantite * lc.prix) AS chiffre_affaire
        FROM commande c
        JOIN adresse a ON c.adresse_id_livre = a.id_adresse
        LEFT JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        GROUP BY dep
        ORDER BY dep
    """

    mycursor.execute(sql)
    stats = mycursor.fetchall()
    print(stats)

    for row in stats:
        row['nb_ventes'] = int(row['nb_ventes'] or 0)
        row['chiffre_affaire'] = float(row['chiffre_affaire'] or 0)

    labels = [row['dep'] for row in stats]
    values_ventes = [row['nb_ventes'] for row in stats]
    values_ca = [row['chiffre_affaire'] for row in stats]

    mycursor.close()

    return render_template(
        'admin/dataviz/dataviz_etat_map.html',
        stats=stats,
        labels=labels,
        values_ventes=values_ventes,
        values_ca=values_ca,
        adresses=stats,
        types_gants_nb=[],
        values=[]
    )


@admin_dataviz.route('/admin/dataviz/etat3')
def show_dataviz_map():
    mycursor = get_db().cursor()

    sql = """
        SELECT
            LEFT(a.code_postal, 2) AS dep,
            COUNT(DISTINCT c.id_commande) AS nb_ventes,
            SUM(lc.quantite * lc.prix) AS chiffre_affaire
        FROM commande c
        JOIN adresse a ON c.adresse_id_livre = a.id_adresse
        LEFT JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        GROUP BY dep
        ORDER BY dep
    """

    mycursor.execute(sql)
    adresses = mycursor.fetchall()

    for row in adresses:
        row['nb_ventes'] = int(row['nb_ventes'] or 0)
        row['chiffre_affaire'] = float(row['chiffre_affaire'] or 0)

    max_ventes = max([r['nb_ventes'] for r in adresses]) if adresses else 1
    max_ca = max([r['chiffre_affaire'] for r in adresses]) if adresses else 1

    for row in adresses:
        row['indice_ventes'] = round(row['nb_ventes'] / max_ventes, 2)
        row['indice_ca'] = round(row['chiffre_affaire'] / max_ca, 2)

    mycursor.close()

    return render_template(
        'admin/dataviz/franceMap.html',

        adresses=adresses,
        labels=[row['dep'] for row in adresses],
        values_ventes=[row['nb_ventes'] for row in adresses],
        values_ca=[row['chiffre_affaire'] for row in adresses],

        # sécurité
        stats=[],
        types_gants_nb=[],
        values=[]
    )