#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                          template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_gant_stock():
    mycursor = get_db().cursor()

    sql_categories = '''
                     SELECT tg.id_type_gant, \
                            tg.nom_type_gant          AS libelle, \
                            COUNT(DISTINCT g.id_gant) AS nbr_gants, \
                            COUNT(DISTINCT n.gant_id) AS nbr_notes, \
                            ROUND(AVG(n.note), 2)     AS note_moyenne, \
                            COUNT(DISTINCT c.gant_id) AS nbr_commentaires
                     FROM type_gant tg
                              LEFT JOIN gant g ON tg.id_type_gant = g.type_gant_id
                              LEFT JOIN note n ON g.id_gant = n.gant_id
                              LEFT JOIN commentaire c ON g.id_gant = c.gant_id
                     GROUP BY tg.id_type_gant, tg.nom_type_gant
                     ORDER BY tg.nom_type_gant \
                     '''
    mycursor.execute(sql_categories)
    categories = mycursor.fetchall()

    sql_gants = '''
                SELECT g.id_gant, \
                       g.nom_gant, \
                       tg.id_type_gant, \
                       tg.nom_type_gant, \
                       COUNT(DISTINCT n.utilisateur_id) AS nbr_notes, \
                       ROUND(AVG(n.note), 2)            AS note_moyenne, \
                       COUNT(DISTINCT CONCAT(c.utilisateur_id, '-', c.date_publication)) \
                                                        AS nbr_commentaires
                FROM gant g
                         JOIN type_gant tg ON g.type_gant_id = tg.id_type_gant
                         LEFT JOIN note n ON g.id_gant = n.gant_id
                         LEFT JOIN commentaire c ON g.id_gant = c.gant_id
                GROUP BY g.id_gant, g.nom_gant, tg.id_type_gant, tg.nom_type_gant
                ORDER BY tg.nom_type_gant, g.nom_gant \
                '''
    mycursor.execute(sql_gants)
    gants = mycursor.fetchall()

    labels_cat = [row['libelle'] for row in categories]
    values_gants = [int(row['nbr_gants']) for row in categories]
    values_notes = [float(row['note_moyenne'] or 0) for row in categories]
    values_nb_notes = [int(row['nbr_notes'] or 0) for row in categories]
    values_nb_commentaires = [int(row['nbr_commentaires'] or 0) for row in categories]

    import json
    gants_par_categorie = {}
    for row in gants:
        cat_id = str(row['id_type_gant'])
        if cat_id not in gants_par_categorie:
            gants_par_categorie[cat_id] = []
        gants_par_categorie[cat_id].append({
            'nom': row['nom_gant'],
            'nbr_notes': int(row['nbr_notes'] or 0),
            'note_moyenne': float(row['note_moyenne'] or 0),
            'nbr_commentaires': int(row['nbr_commentaires'] or 0),
        })

    mycursor.close()

    return render_template(
        'admin/dataviz/dataviz_etat_1.html',
        types_gants_nb=categories,
        labels=json.dumps(labels_cat),
        values=json.dumps(values_gants),
        categories=categories,
        labels_cat=json.dumps(labels_cat),
        values_notes=json.dumps(values_notes),
        values_nb_notes=json.dumps(values_nb_notes),
        values_nb_commentaires=json.dumps(values_nb_commentaires),
        gants_par_categorie=json.dumps(gants_par_categorie),
    )


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)
    mycursor.close()
    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                           )


