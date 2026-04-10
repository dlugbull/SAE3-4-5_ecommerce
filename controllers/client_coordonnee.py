from flask import Blueprint, request, render_template, redirect, flash, session
from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__, template_folder='templates')


def compter_adresses_valides(cursor, user_id):
    cursor.execute("""
                   SELECT COUNT(*) as nb
                   FROM adresse
                   WHERE utilisateur_id = %s
                     AND est_valide = TRUE
                   """, (user_id,))
    return cursor.fetchone()['nb']


def set_favori(cursor, user_id, id_adresse):
    cursor.execute("""
                   UPDATE adresse
                   SET est_favori = FALSE
                   WHERE utilisateur_id = %s
                   """, (user_id,))

    cursor.execute("""
                   UPDATE adresse
                   SET est_favori = TRUE
                   WHERE id_adresse = %s
                   """, (id_adresse,))


@client_coordonnee.route('/client/coordonnee/show')
def show():
    cursor = get_db().cursor()
    user_id = session['id_user']

    cursor.execute("SELECT * FROM utilisateur WHERE id_utilisateur=%s", (user_id,))
    utilisateur = cursor.fetchone()

    cursor.execute("""
                   SELECT a.*,
                          COUNT(c.id_commande) as nbr_commandes
                   FROM adresse a
                            LEFT JOIN commande c ON a.id_adresse = c.adresse_id_livre
                   WHERE a.utilisateur_id = %s
                   GROUP BY a.id_adresse
                   ORDER BY a.est_favori DESC, a.id_adresse DESC
                   """, (user_id,))

    adresses = cursor.fetchall()

    nb_valides = compter_adresses_valides(cursor, user_id)
    nb_total = len(adresses)

    cursor.close()
    return render_template("client/coordonnee/show_coordonnee.html",
                           utilisateur=utilisateur,
                           adresses=adresses,
                           nb_adresses=nb_valides,
                           nb_adresses_tot=nb_total)


@client_coordonnee.route('/client/coordonnee/add_adresse', methods=['POST'])
def add():
    cursor = get_db().cursor()
    user_id = session['id_user']

    nom = request.form['nom']
    rue = request.form['rue']
    cp = request.form['code_postal']
    ville = request.form['ville']

    if not cp.isdigit() or len(cp) != 5:
        flash("Code postal invalide", "alert-warning")
        return redirect('/client/coordonnee/show')

    if compter_adresses_valides(cursor, user_id) >= 4:
        flash("Max 4 adresses atteintes", "alert-warning")
        return redirect('/client/coordonnee/show')

    cursor.execute("""
                   INSERT INTO adresse (nom_adresse, rue, code_postal, ville, utilisateur_id)
                   VALUES (%s, %s, %s, %s, %s)
                   """, (nom, rue, cp, ville, user_id))

    new_id = cursor.lastrowid
    set_favori(cursor, user_id, new_id)

    get_db().commit()
    cursor.close()

    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse', methods=['POST'])
def delete():
    cursor = get_db().cursor()
    user_id = session['id_user']
    id_adresse = request.form['id_adresse']

    cursor.execute("""
                   SELECT *
                   FROM adresse
                   WHERE id_adresse = %s
                     AND utilisateur_id = %s
                   """, (id_adresse, user_id))

    if not cursor.fetchone():
        flash("Erreur sécurité", "alert-danger")
        return redirect('/client/coordonnee/show')

    cursor.execute("""
                   SELECT COUNT(*) as nb
                   FROM commande
                   WHERE adresse_id_livre = %s
                      OR adresse_id_fact = %s
                   """, (id_adresse, id_adresse))

    used = cursor.fetchone()['nb'] > 0

    if used:
        cursor.execute("""
                       UPDATE adresse
                       SET est_valide = FALSE
                       WHERE id_adresse = %s
                       """, (id_adresse,))
    else:
        cursor.execute("DELETE FROM adresse WHERE id_adresse=%s", (id_adresse,))

    get_db().commit()
    cursor.close()
    return redirect('/client/coordonnee/show')