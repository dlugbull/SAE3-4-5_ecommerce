#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_gant = Blueprint('admin_gant', __name__,
                          template_folder='templates')


@admin_gant.route('/admin/gant/show')
def show_gant():
    mycursor = get_db().cursor()
    sql = '''  requête admin_gant_1
    '''
    mycursor.execute(sql)
    gants = mycursor.fetchall()
    return render_template('admin/gant/show_gant.html', gants=gants)


@admin_gant.route('/admin/gant/add', methods=['GET'])
def add_gant():
    mycursor = get_db().cursor()

    return render_template('admin/gant/add_gant.html'
                           #,types_gant=type_gant,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_gant.route('/admin/gant/add', methods=['POST'])
def valid_add_gant():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_gant_id = request.form.get('type_gant_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_gant_2 '''

    tuple_add = (nom, filename, prix, type_gant_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'gant ajouté , nom: ', nom, ' - type_gant:', type_gant_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'gant ajouté , nom:' + nom + '- type_gant:' + type_gant_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/gant/show')


@admin_gant.route('/admin/gant/delete', methods=['GET'])
def delete_gant():
    id_gant=request.args.get('id_gant')
    mycursor = get_db().cursor()
    sql = ''' requête admin_gant_3 '''
    mycursor.execute(sql, id_gant)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet gant : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_gant_4 '''
        mycursor.execute(sql, id_gant)
        gant = mycursor.fetchone()
        print(gant)
        image = gant['image']

        sql = ''' requête admin_gant_5  '''
        mycursor.execute(sql, id_gant)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un gant supprimé, id :", id_gant)
        message = u'un gant supprimé, id : ' + id_gant
        flash(message, 'alert-success')

    return redirect('/admin/gant/show')


@admin_gant.route('/admin/gant/edit', methods=['GET'])
def edit_gant():
    id_gant=request.args.get('id_gant')
    mycursor = get_db().cursor()
    sql = '''
    requête admin_gant_6    
    '''
    mycursor.execute(sql, id_gant)
    gant = mycursor.fetchone()
    print(gant)
    sql = '''
    requête admin_gant_7
    '''
    mycursor.execute(sql)
    types_gant = mycursor.fetchall()

    # sql = '''
    # requête admin_gant_6
    # '''
    # mycursor.execute(sql, id_gant)
    # declinaisons_gant = mycursor.fetchall()

    return render_template('admin/gant/edit_gant.html'
                           ,gant=gant
                           ,types_gant=types_gant
                         #  ,declinaisons_gant=declinaisons_gant
                           )


@admin_gant.route('/admin/gant/edit', methods=['POST'])
def valid_edit_gant():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_gant = request.form.get('id_gant')
    image = request.files.get('image', '')
    type_gant_id = request.form.get('type_gant_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       requête admin_gant_8
       '''
    mycursor.execute(sql, id_gant)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''  requête admin_gant_9 '''
    mycursor.execute(sql, (nom, image_nom, prix, type_gant_id, description, id_gant))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'gant modifié , nom:' + nom + '- type_gant :' + type_gant_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/gant/show')







@admin_gant.route('/admin/gant/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    gant=[]
    commentaires = {}
    return render_template('admin/gant/show_avis.html'
                           , gant=gant
                           , commentaires=commentaires
                           )


@admin_gant.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    gant_id = request.form.get('idgant', None)
    userId = request.form.get('idUser', None)

    return admin_avis(gant_id)
