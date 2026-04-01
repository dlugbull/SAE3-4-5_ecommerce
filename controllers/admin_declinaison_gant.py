#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_gant = Blueprint('admin_declinaison_gant', __name__,
                                   template_folder='templates')


@admin_declinaison_gant.route('/admin/declinaison_gant/add')
def add_declinaison_gant():
    id_gant=request.args.get('id_gant')
    mycursor = get_db().cursor()
    sql = '''SELECT gant.id_gant, gant.photo as image
             FROM gant
             WHERE id_gant=%s'''
    mycursor.execute(sql, (id_gant,))
    gant=mycursor.fetchone()
    sql = '''SELECT id_couleur, libelle_couleur as libelle
             FROM couleur
             WHERE id_couleur<>1'''
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()

    sql = '''SELECT id_taille, concat('fr : ', taille.num_taille_fr, ', us : ', taille.taille_us, ', tour de main : ', taille.tour_de_main) as libelle
             FROM taille
             WHERE id_taille<>1'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    sql = '''SELECT taille_id
             FROM declinaison_gant
             WHERE gant_id=%s AND taille_id=1'''
    mycursor.execute(sql, id_gant)
    id_taille = mycursor.fetchone()

    sql = '''SELECT couleur_id
             FROM declinaison_gant
             WHERE gant_id = %s AND couleur_id = 1'''
    mycursor.execute(sql, id_gant)
    id_couleur = mycursor.fetchone()

    d_taille_uniq=id_taille['taille_id'] if id_taille is not None else None
    d_couleur_uniq=id_couleur['couleur_id'] if id_couleur is not None else None
    mycursor.close()
    return render_template('admin/gant/add_declinaison_gant.html'
                           , gant=gant
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_gant.route('/admin/declinaison_gant/add', methods=['POST'])
def valid_add_declinaison_gant():
    mycursor = get_db().cursor()

    id_gant = request.form.get('id_gant')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')

    sql = '''SELECT *
             FROM declinaison_gant
             WHERE gant_id = %s AND taille_id=%s AND couleur_id=%s'''
    mycursor.execute(sql, (id_gant,taille,couleur))
    test = mycursor.fetchone()
    if test is not None:
        sql = '''UPDATE declinaison_gant
                 SET stock=%s
                 WHERE id_declinaison_gant=%s'''
        mycursor.execute(sql, (stock, test['id_declinaison_gant']))
    else:
        sql = '''INSERT INTO declinaison_gant VALUES
            (null, %s, (SELECT gant.prix_gant
                        FROM gant
                        WHERE id_gant=%s), null, %s, %s, %s)'''
        mycursor.execute(sql, (stock, id_gant,taille, couleur, id_gant))
        flash(f'Declinaison ajoutée : stock : {stock}, taille : {taille}, couleur : {couleur}, pour le gant d\'id {id_gant}', 'alert-success')

    # attention au doublon
    get_db().commit()
    mycursor.close()
    return redirect('/admin/gant/edit?id_gant=' + id_gant)


@admin_declinaison_gant.route('/admin/declinaison_gant/edit', methods=['GET'])
def edit_declinaison_gant():
    id_declinaison_gant = request.args.get('id_declinaison_gant')
    mycursor = get_db().cursor()
    sql = '''SELECT gant.nom_gant as nom, gant.photo as image_gant,
                    declinaison_gant.id_declinaison_gant, declinaison_gant.gant_id,
                    declinaison_gant.stock, declinaison_gant.taille_id,
                    declinaison_gant.couleur_id
             FROM declinaison_gant
                      JOIN gant ON declinaison_gant.gant_id = gant.id_gant'''
    mycursor.execute(sql)
    declinaison_gant=mycursor.fetchone()

    sql = '''SELECT id_couleur, libelle_couleur as libelle
             FROM couleur
             WHERE id_couleur <> 1'''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()

    sql = '''SELECT id_taille, \
                    concat('fr : ', taille.num_taille_fr, ', us : ', taille.taille_us, ', tour de main : ', \
                           taille.tour_de_main) as libelle
             FROM taille
             WHERE id_taille <> 1'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    sql = '''SELECT taille_id
             FROM declinaison_gant
             WHERE gant_id = (select gant_id
                              from declinaison_gant
                              WHERE id_declinaison_gant=%s)
               AND taille_id = 1'''
    mycursor.execute(sql, id_declinaison_gant)
    id_taille = mycursor.fetchone()

    sql = '''SELECT couleur_id
             FROM declinaison_gant
             WHERE gant_id = (select gant_id
                              from declinaison_gant
                              WHERE id_declinaison_gant=%s)
               AND couleur_id = 1'''
    mycursor.execute(sql, id_declinaison_gant)
    id_couleur = mycursor.fetchone()

    d_taille_uniq = id_taille['taille_id'] if id_taille is not None else None
    d_couleur_uniq = id_couleur['couleur_id'] if id_couleur is not None else None
    mycursor.close()
    return render_template('admin/gant/edit_declinaison_gant.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_gant=declinaison_gant
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_gant.route('/admin/declinaison_gant/edit', methods=['POST'])
def valid_edit_declinaison_gant():
    id_declinaison_gant = request.form.get('id_declinaison_gant','')
    id_gant = request.form.get('id_gant','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    sql = '''SELECT *
             FROM declinaison_gant
             WHERE taille_id = %s AND couleur_id = %s AND gant_id = %s'''
    mycursor.execute(sql, (taille_id, couleur_id, id_gant))
    test = mycursor.fetchone()
    if test is not None:
        sql = '''UPDATE declinaison_gant
                 SET stock=%s
                 WHERE taille_id = %s AND couleur_id = %s AND gant_id = %s'''
        mycursor.execute(sql, (stock, taille_id, couleur_id, id_gant))
    else:
        sql = '''UPDATE declinaison_gant
                 SET stock=%s, taille_id=%s, couleur_id=%s
                 WHERE id_declinaison_gant=%s'''
        mycursor.execute(sql, (stock, taille_id, couleur_id, id_declinaison_gant))

    message = u'declinaison_gant modifié , id:' + str(id_declinaison_gant) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    mycursor.close()
    return redirect('/admin/gant/edit?id_gant=' + str(id_gant))


@admin_declinaison_gant.route('/admin/declinaison_gant/delete', methods=['GET'])
def admin_delete_declinaison_gant():
    id_declinaison_gant = request.args.get('id_declinaison_gant','')
    id_gant = request.args.get('id_gant','')
    mycursor = get_db().cursor()

    sql = '''SELECT *
             FROM ligne_commande
             WHERE declinaison_gant_id=%s'''
    mycursor.execute(sql, (id_declinaison_gant,))
    commande = mycursor.fetchone()
    if commande is not None:
        flash('Cette déclinaison est commandée : elle ne peut pas être supprimée')
    else:
        sql = '''DELETE FROM ligne_panier
                 WHERE declinaison_gant_id=%s'''
        mycursor.execute(sql, (id_declinaison_gant,))
        sql = '''DELETE FROM declinaison_gant
                 WHERE id_declinaison_gant=%s'''
        mycursor.execute(sql, (id_declinaison_gant,))
        flash(u'declinaison supprimée, id_declinaison_gant : ' + str(id_declinaison_gant), 'alert-success')

    get_db().commit()
    mycursor.close()
    return redirect('/admin/gant/edit?id_gant=' + str(id_gant))
