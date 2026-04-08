#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/gant/details', methods=['GET'])
def client_gant_details():
    mycursor = get_db().cursor()
    id_gant =  request.args.get('id_gant', None)
    id_client = session['id_user']

    ## partie 4
    # client_historique_add(id_gant, id_client)

    sql = '''
            SELECT  g.*,
                    g.id_gant,
                    AVG(n.note)                        AS moyenne_notes,
                    COUNT(n.note)                      AS nb_notes
            FROM gant g
            LEFT JOIN note n ON n.gant_id = g.id_gant
            WHERE g.id_gant = %s
            GROUP BY g.id_gant
          '''
    mycursor.execute(sql, (id_gant,))
    gant = mycursor.fetchone()

    commandes_gants = []
    nb_commentaires = []
    if gant is None:
        abort(404, "pb id gant")

    sql = '''
    SELECT  c.*,
            u.nom_utilisateur AS nom,
            u.id_utilisateur,
            g.id_gant
    FROM commentaire c
    JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
    JOIN gant g ON g.id_gant = c.gant_id
    WHERE c.gant_id = %s
    AND (c.valider = TRUE OR c.utilisateur_id = %s)
    ORDER BY c.date_publication DESC
    '''
    mycursor.execute(sql, ( id_gant, id_client))
    commentaires = mycursor.fetchall()

    sql = '''
    SELECT COUNT(DISTINCT lc.commande_id) AS nb_commandes_gant
    FROM ligne_commande lc
    JOIN declinaison_gant dg ON dg.id_declinaison_gant = lc.declinaison_gant_id
    JOIN commande c ON c.id_commande = lc.commande_id
    WHERE c.utilisateur_id = %s AND dg.gant_id = %s
    '''
    mycursor.execute(sql, (id_client, id_gant))
    commandes_gants = mycursor.fetchone()

    sql = '''
    SELECT n.note
    FROM note n
    WHERE n.utilisateur_id = %s AND n.gant_id = %s
    '''
    mycursor.execute(sql, (id_client, id_gant))
    note = mycursor.fetchone()
    print('note',note)
    if note:
        note=note['note']

    sql = '''
    SELECT  COUNT(CASE WHEN c.utilisateur_id = %s THEN 1 END) AS nb_commentaires_utilisateur ,
            COUNT(*) AS nb_commentaires_total,
            COUNT(CASE WHEN c.utilisateur_id = %s AND c.valider = 1 THEN 1 END) AS nb_commentaires_utilisateur_valide,
            COUNT(CASE WHEN c.valider = 1 THEN 1 END) AS nb_commentaires_total_valide
    FROM commentaire c
    WHERE c.gant_id = %s
    '''
    mycursor.execute(sql, (id_client, id_client, id_gant))
    nb_commentaires = mycursor.fetchone()

    mycursor.close()
    return render_template('client/gant_info/article_details.html'
                            , gant=gant
                            , commentaires=commentaires
                            , commandes_gants=commandes_gants
                            , note=note
                            , nb_commentaires=nb_commentaires
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_gant = request.form.get('id_gant', None)

    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        mycursor.close()
        return redirect('/client/gant/details?id_gant='+id_gant)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')
        mycursor.close()
        return redirect('/client/gant/details?id_gant='+id_gant)

    tuple_insert = (commentaire, id_client, id_gant)
    sql = '''
        INSERT INTO commentaire (commentaire, utilisateur_id, gant_id, date_publication, valider)
        VALUES (%s, %s, %s, NOW(), FALSE)
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    mycursor.close()
    return redirect('/client/gant/details?id_gant='+id_gant)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_gant = request.form.get('id_gant', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''
        DELETE FROM commentaire
        WHERE utilisateur_id = %s AND gant_id = %s AND date_publication = %s
    '''
    tuple_delete=(id_client,id_gant,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    mycursor.close()
    return redirect('/client/gant/details?id_gant='+id_gant)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_gant = request.form.get('id_gant', None)
    tuple_insert = (note, id_client, id_gant)
    print(tuple_insert)
    sql = '''
        INSERT INTO note (note, utilisateur_id, gant_id)
        VALUES (%s, %s, %s)
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    mycursor.close()
    return redirect('/client/gant/details?id_gant='+id_gant)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_gant = request.form.get('id_gant', None)
    tuple_update = (note, id_client, id_gant)
    print(tuple_update)
    sql = '''
        UPDATE note SET note = %s
        WHERE utilisateur_id = %s AND gant_id = %s
    '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    mycursor.close()
    return redirect('/client/gant/details?id_gant='+id_gant)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_gant = request.form.get('id_gant', None)
    tuple_delete = (id_client, id_gant)
    print(tuple_delete)
    sql = '''
        DELETE FROM note
        WHERE utilisateur_id = %s AND gant_id = %s
    '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    mycursor.close()
    return redirect('/client/gant/details?id_gant='+id_gant)
