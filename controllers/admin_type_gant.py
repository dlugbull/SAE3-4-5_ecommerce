#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_gant = Blueprint('admin_type_gant', __name__,
                        template_folder='templates')

@admin_type_gant.route('/admin/type-gant/show')
def show_type_gant():
    mycursor = get_db().cursor()
    # sql = '''         '''
    # mycursor.execute(sql)
    # types_gant = mycursor.fetchall()
    types_gant=[]
    return render_template('admin/type_gant/show_type_gant.html', types_gant=types_gant)

@admin_type_gant.route('/admin/type-gant/add', methods=['GET'])
def add_type_gant():
    return render_template('admin/type_gant/add_type_gant.html')

@admin_type_gant.route('/admin/type-gant/add', methods=['POST'])
def valid_add_type_gant():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    mycursor = get_db().cursor()
    sql = '''         '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-gant/show') #url_for('show_type_gant')

@admin_type_gant.route('/admin/type-gant/delete', methods=['GET'])
def delete_type_gant():
    id_type_gant = request.args.get('id_type_gant', '')
    mycursor = get_db().cursor()

    flash(u'suppression type gant , id : ' + id_type_gant, 'alert-success')
    return redirect('/admin/type-gant/show')

@admin_type_gant.route('/admin/type-gant/edit', methods=['GET'])
def edit_type_gant():
    id_type_gant = request.args.get('id_type_gant', '')
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, (id_type_gant,))
    type_gant = mycursor.fetchone()
    return render_template('admin/type_gant/edit_type_gant.html', type_gant=type_gant)

@admin_type_gant.route('/admin/type-gant/edit', methods=['POST'])
def valid_edit_type_gant():
    libelle = request.form['libelle']
    id_type_gant = request.form.get('id_type_gant', '')
    tuple_update = (libelle, id_type_gant)
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type gant modifié, id: ' + id_type_gant + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-gant/show')








