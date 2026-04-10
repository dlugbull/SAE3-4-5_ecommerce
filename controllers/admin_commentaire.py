#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/gant/commentaires', methods=['GET'])
def admin_gant_details():
    mycursor = get_db().cursor()
    id_gant =  request.args.get('id_gant', None)
    sql = '''
    SELECT c.utilisateur_id AS id_utilisateur,
           u.nom_utilisateur AS nom,
           c.gant_id AS id_gant,
           c.date_publication AS date_publication,
           c.commentaire AS commentaire,
           c.valider AS valider
    FROM commentaire c
    JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
    WHERE c.gant_id = %s
    ORDER BY    c.valider ASC, c.date_publication DESC, c.utilisateur_id DESC;
          '''
    mycursor.execute(sql, (id_gant,))
    commentaires = mycursor.fetchall()

    sql = '''
    SELECT g.id_gant,
           g.nom_gant AS nom,
           AVG(n.note)   AS moyenne_notes,
           COUNT(n.note) AS nb_notes
    FROM gant g
    LEFT JOIN note n ON n.gant_id = g.id_gant
    WHERE g.id_gant = %s
    GROUP BY g.id_gant, g.nom_gant
          '''
    mycursor.execute(sql, (id_gant,))
    gant = mycursor.fetchone()

    sql = '''
    SELECT COUNT(*)                     AS nb_commentaires_total,
           SUM(IF(valider = 1, 1, 0))   AS nb_commentaires_valider
    FROM commentaire
    WHERE gant_id = %s AND utilisateur_id != 1
          '''
    mycursor.execute(sql, (id_gant,))
    nb_commentaires = mycursor.fetchone()

    mycursor.close()
    print(commentaires)
    return render_template('admin/gant/show_gant_commentaires.html'
                           , commentaires=commentaires
                           , gant=gant
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/gant/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_gant = request.form.get('id_gant', None)
    date_publication = request.form.get('date_publication', None)

    sql = '''
    DELETE FROM commentaire
    WHERE utilisateur_id = %s AND gant_id = %s AND date_publication = %s
    '''
    mycursor.execute(sql, (id_utilisateur, id_gant, date_publication))

    get_db().commit()
    mycursor.close()
    return redirect('/admin/gant/commentaires?id_gant=' + id_gant)


@admin_commentaire.route('/admin/gant/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_gant = request.args.get('id_gant', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/gant/add_commentaire.html',id_utilisateur=id_utilisateur,id_gant=id_gant,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_gant = request.form.get('id_gant', None)
    date_publication = request.form.get('date_publication', None)

    sql1 = '''
           SELECT COUNT(*) as nb
           FROM commentaire
           WHERE gant_id = %s AND date_publication = %s AND utilisateur_id = 1 \
           '''
    mycursor.execute(sql1, (id_gant, date_publication))
    result = mycursor.fetchone()

    if result['nb'] > 0:
        flash("Information : vous avez deja répondu, supprimer et recréer votre réponse", 'alert-warning')
        mycursor.close()
        return redirect('/admin/gant/commentaires?id_gant=' + id_gant)

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_gant = request.form.get('id_gant', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''
        INSERT INTO commentaire (utilisateur_id, gant_id, date_publication, commentaire, valider)
        VALUES (%s, %s, %s, %s, TRUE)
    '''
    mycursor.execute(sql, (id_utilisateur, id_gant, date_publication, commentaire))
    get_db().commit()
    mycursor.close()
    return redirect('/admin/gant/commentaires?id_gant='+id_gant)


@admin_commentaire.route('/admin/gant/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_gant = request.args.get('id_gant', None)
    mycursor = get_db().cursor()
    sql = '''
        UPDATE commentaire
        SET valider = TRUE
        WHERE gant_id = %s AND utilisateur_id != 1   
    '''
    mycursor.execute(sql, (id_gant,))
    get_db().commit()
    mycursor.close()
    return redirect('/admin/gant/commentaires?id_gant='+id_gant)