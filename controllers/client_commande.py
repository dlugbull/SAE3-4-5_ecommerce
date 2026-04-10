#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, flash, session
from datetime import datetime

from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                            template_folder='templates')



@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = """
        SELECT declinaison_gant.id_declinaison_gant,
               gant.nom_gant AS nom,
               declinaison_gant.prix_declinaison AS prix,
               ligne_panier.quantite
        FROM gant
        JOIN declinaison_gant ON gant.id_gant = declinaison_gant.gant_id
        JOIN ligne_panier ON declinaison_gant.id_declinaison_gant = ligne_panier.declinaison_gant_id
        WHERE ligne_panier.utilisateur_id = %s
    """
    mycursor.execute(sql, (id_client,))
    gants_panier = mycursor.fetchall()

    if len(gants_panier) >= 1:
        sql = """
            SELECT SUM(prix_declinaison * quantite) AS prix_total
            FROM declinaison_gant
            JOIN ligne_panier ON declinaison_gant.id_declinaison_gant = ligne_panier.declinaison_gant_id
            WHERE ligne_panier.utilisateur_id = %s
        """
        mycursor.execute(sql, (id_client,))
        prix_total = mycursor.fetchone()["prix_total"]
    else:
        prix_total = None

    sql = """
        SELECT id_adresse,
               nom_adresse AS nom,
               rue,
               code_postal,
               ville,
               IF(date_utilisation = (
                   SELECT MAX(a2.date_utilisation)
                   FROM adresse a2
                   WHERE a2.utilisateur_id = %s
                     AND a2.date_utilisation != '2000-01-01'
               ), 1, 0) AS favori
        FROM adresse
        WHERE utilisateur_id = %s
          AND date_utilisation != '2000-01-01'
        ORDER BY date_utilisation DESC
    """
    mycursor.execute(sql, (id_client, id_client))
    adresses = mycursor.fetchall()

    id_adresse_fav = None
    for a in adresses:
        if int(a['favori']) == 1:
            id_adresse_fav = a['id_adresse']
            break

    mycursor.close()
    return render_template(
        'client/boutique/panier_validation_adresses.html',
        adresses=adresses,
        gants_panier=gants_panier,
        prix_total=prix_total,
        validation=1,
        id_adresse_fav=id_adresse_fav
    )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    id_adresse_livraison = request.form.get('id_adresse_livraison')
    id_adresse_facturation = request.form.get('id_adresse_facturation')

    for id_adr in [id_adresse_livraison, id_adresse_facturation]:
        sql = "SELECT COUNT(*) AS nb FROM adresse WHERE id_adresse = %s AND utilisateur_id = %s"
        mycursor.execute(sql, (id_adr, id_client))
        if mycursor.fetchone()['nb'] == 0:
            flash("Adresse invalide.", "alert-danger")
            mycursor.close()
            return redirect('/client/gant/show')

    sql = """
        SELECT *, quantite * prix_declinaison AS prix
        FROM ligne_panier
        JOIN declinaison_gant ON ligne_panier.declinaison_gant_id = declinaison_gant.id_declinaison_gant
        WHERE utilisateur_id = %s
    """
    mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()

    if not items_panier or len(items_panier) < 1:
        flash("Pas de gants dans le panier.", "alert-warning")
        mycursor.close()
        return redirect('/client/gant/show')

    sql = """
        INSERT INTO commande (date_achat, etat_id, utilisateur_id, adresse_id_livre, adresse_id_fact)
        VALUES (%s, 1, %s, %s, %s)
    """
    mycursor.execute(sql, (datetime.now(), id_client, id_adresse_livraison, id_adresse_facturation))
    get_db().commit()

    sql = "SELECT last_insert_id() AS last_insert_id"
    mycursor.execute(sql)
    id_commande = mycursor.fetchone()['last_insert_id']

    for item in items_panier:
        sql = """
            DELETE FROM ligne_panier
            WHERE declinaison_gant_id = %s AND utilisateur_id = %s
        """
        mycursor.execute(sql, (item["id_declinaison_gant"], item["utilisateur_id"]))
        sql = """
            INSERT INTO ligne_commande (commande_id, declinaison_gant_id, quantite, prix)
            VALUES (%s, %s, %s, %s)
        """
        mycursor.execute(sql, (id_commande, item["id_declinaison_gant"], item["quantite"], item["prix"]))

    get_db().commit()

    sql = """
        UPDATE adresse
        SET date_utilisation = NOW()
        WHERE id_adresse = %s AND utilisateur_id = %s
    """
    mycursor.execute(sql, (id_adresse_livraison, id_client))
    get_db().commit()

    flash("Commande passée avec succès !", "alert-success")
    mycursor.close()
    return redirect('/client/gant/show')


@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = """
        SELECT commande.etat_id,
               utilisateur.login,
               SUM(ligne_commande.quantite) AS nbr_gants,
               SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total,
               commande.date_achat,
               etat.libelle_etat AS libelle,
               commande.id_commande
        FROM commande
        JOIN utilisateur ON utilisateur.id_utilisateur = commande.utilisateur_id
        JOIN ligne_commande ON ligne_commande.commande_id = commande.id_commande
        JOIN etat ON etat.id_etat = commande.etat_id
        WHERE commande.utilisateur_id = %s
        GROUP BY commande.id_commande
        ORDER BY etat_id, date_achat DESC
    """
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    gants_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)

    if id_commande is not None:
        sql = """
            SELECT gant.nom_gant AS nom,
                   ligne_commande.quantite,
                   ligne_commande.prix,
                   (ligne_commande.quantite * ligne_commande.prix) AS prix_ligne,
                   commande.etat_id,
                   commande.id_commande AS id,
                   couleur.id_couleur,
                   couleur.libelle_couleur,
                   couleur.code_couleur,
                   taille.id_taille,
                   CONCAT('fr : ', taille.num_taille_fr, ', us : ', taille.taille_us, ', tour de main : ', taille.tour_de_main) AS libelle_taille,
                   (SELECT COUNT(gant_id) FROM declinaison_gant WHERE declinaison_gant.gant_id = id_gant) AS nb_declinaisons
            FROM ligne_commande
            JOIN declinaison_gant ON ligne_commande.declinaison_gant_id = declinaison_gant.id_declinaison_gant
            JOIN couleur ON declinaison_gant.couleur_id = couleur.id_couleur
            JOIN taille ON declinaison_gant.taille_id = taille.id_taille
            JOIN gant ON declinaison_gant.gant_id = gant.id_gant
            JOIN commande ON commande.id_commande = ligne_commande.commande_id
            WHERE ligne_commande.commande_id = %s AND commande.utilisateur_id = %s
        """
        mycursor.execute(sql, (id_commande, id_client))
        gants_commande = mycursor.fetchall()

        if not gants_commande:
            flash("Cette commande ne vous appartient pas.", "alert-warning")

        sql = """
            SELECT a_fact.nom_adresse AS nom_facturation,
                   a_fact.rue AS rue_facturation,
                   a_fact.code_postal AS code_postal_facturation,
                   a_fact.ville AS ville_facturation,
                   a_livre.nom_adresse AS nom_livraison,
                   a_livre.rue AS rue_livraison,
                   a_livre.code_postal AS code_postal_livraison,
                   a_livre.ville AS ville_livraison,
                   IF(a_livre.id_adresse = a_fact.id_adresse, 'adresse_identique', NULL) AS adresse_identique
            FROM commande
            JOIN adresse a_fact ON a_fact.id_adresse = commande.adresse_id_fact
            JOIN adresse a_livre ON a_livre.id_adresse = commande.adresse_id_livre
            WHERE commande.utilisateur_id = %s AND commande.id_commande = %s
        """
        mycursor.execute(sql, (id_client, id_commande))
        commande_adresses = mycursor.fetchone()

    mycursor.close()
    return render_template(
        'client/commandes/show.html',
        commandes=commandes,
        gants_commande=gants_commande,
        commande_adresses=commande_adresses
    )