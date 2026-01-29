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
    sql = '''    requête admin_type_gant_1    '''
    commentaires = {}
    sql = '''   requête admin_type_gant_1_bis   '''
    gant = []
    sql = '''   requête admin_type_gant_1_3   '''
    nb_commentaires = []
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
    sql = '''    requête admin_type_gant_2   '''
    tuple_delete=(id_utilisateur,id_gant,date_publication)
    get_db().commit()
    return redirect('/admin/gant/commentaires?id_gant='+id_gant)


@admin_commentaire.route('/admin/gant/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_gant = request.args.get('id_gant', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/gant/add_commentaire.html',id_utilisateur=id_utilisateur,id_gant=id_gant,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_gant = request.form.get('id_gant', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_gant_3   '''
    get_db().commit()
    return redirect('/admin/gant/commentaires?id_gant='+id_gant)


@admin_commentaire.route('/admin/gant/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_gant = request.args.get('id_gant', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_type_gant_4   '''
    get_db().commit()
    return redirect('/admin/gant/commentaires?id_gant='+id_gant)