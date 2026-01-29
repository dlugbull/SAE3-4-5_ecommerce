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
    gant=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
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
    # attention au doublon
    get_db().commit()
    return redirect('/admin/gant/edit?id_gant=' + id_gant)


@admin_declinaison_gant.route('/admin/declinaison_gant/edit', methods=['GET'])
def edit_declinaison_gant():
    id_declinaison_gant = request.args.get('id_declinaison_gant')
    mycursor = get_db().cursor()
    declinaison_gant=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
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

    message = u'declinaison_gant modifié , id:' + str(id_declinaison_gant) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/gant/edit?id_gant=' + str(id_gant))


@admin_declinaison_gant.route('/admin/declinaison_gant/delete', methods=['GET'])
def admin_delete_declinaison_gant():
    id_declinaison_gant = request.args.get('id_declinaison_gant','')
    id_gant = request.args.get('id_gant','')

    flash(u'declinaison supprimée, id_declinaison_gant : ' + str(id_declinaison_gant),  'alert-success')
    return redirect('/admin/gant/edit?id_gant=' + str(id_gant))
