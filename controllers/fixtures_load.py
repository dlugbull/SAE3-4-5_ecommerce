#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    # Suppression des tables dans l'ordre inverse des dépendances
    sql = '''DROP TABLE IF EXISTS ligne_panier'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS ligne_commande'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS gant'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS commande'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS type_gant'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS taille'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS etat'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS utilisateur'''
    mycursor.execute(sql)

    # Création de la table utilisateur
    sql = '''
    CREATE TABLE utilisateur(
        id_utilisateur INTEGER AUTO-INCREMENT,
        login VARCHAR(50),
        email VARCHAR(50),
        nom_utilisateur VARCHAR(50),
        password VARCHAR(255),
        role VARCHAR(50),
        PRIMARY KEY(id_utilisateur)
    ) DEFAULT CHARSET utf8;
    '''
    mycursor.execute(sql)

    # Insertion des utilisateurs
    sql = '''
    INSERT INTO utilisateur VALUES
        ('U001', 'admin', 'admin@boutique-gants.fr', 'Administrateur', 'pbkdf2:sha256:1000000$qwwvIJXyTvBTH4R1$73dd8f46cc5953965c9befed035509d47bb89b18166d02c2ee6b0924fb18f923', 'admin'),
        ('U002', 'client', 'client@email.com', 'Sophie Martin', 'pbkdf2:sha256:1000000$9u2VVssEqRYwvrze$b3ef9670d06f24ed3dc11a92f1cca4c7b00dd5c301d13bbedec2d6f1f0bb6eb0', 'client'),
        ('U003', 'client2', 'client2@email.com', 'Thomas Dubois', 'pbkdf2:sha256:1000000$Eq13PRiR0mkFGUej$4df2d53f486dc29e78c65a6ea3cc7004c4343bc58cdb8c91c19d43a3f84399fe', 'client')
    '''
    mycursor.execute(sql)

    # Création de la table etat
    sql = '''
    CREATE TABLE etat(
        id_etat INT,
        libelle_etat VARCHAR(50),
        PRIMARY KEY(id_etat)
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    # Insertion des états
    sql = '''
    INSERT INTO etat VALUES
        (1, 'En attente'),
        (2, 'Expédiée')
    '''
    mycursor.execute(sql)

    # Création de la table taille
    sql = '''
    CREATE TABLE taille(
        id_taille INT,
        num_taille_fr VARCHAR(50),
        taille_us VARCHAR(50),
        tour_de_main VARCHAR(50),
        PRIMARY KEY(id_taille)
    ) DEFAULT CHARSET utf8;
    '''
    mycursor.execute(sql)

    # Insertion des tailles
    sql = '''
    INSERT INTO taille VALUES
        (1, '6', 'XS', '15-16 cm'),
        (2, '7', 'XS/S', '16-17 cm'),
        (3, '8', 'S', '17-18 cm'),
        (4, '9', 'S/M', '18-19 cm'),
        (5, '10', 'M', '19-20 cm'),
        (6, '11', 'M/L', '20-21 cm'),
        (7, '12', 'L', '21-22 cm'),
        (8, '13', 'L/XL', '22-23 cm'),
        (9, '14', 'XL', '23-24 cm'),
        (10, '15', 'XL/XXL', '24-25 cm')
    '''
    mycursor.execute(sql)

    # Création de la table type_gant
    sql = '''
    CREATE TABLE type_gant(
        id_type_gant INT,
        nom_type_gant VARCHAR(255),
        PRIMARY KEY(id_type_gant)
    ) DEFAULT CHARSET utf8;
    '''
    mycursor.execute(sql)

    # Insertion des types de gants
    sql = '''
    INSERT INTO type_gant VALUES
        (1, 'Gants de Vélo'),
        (2, 'Gants de Sport Combat'),
        (3, 'Gants d\'\'Hiver'),
        (4, 'Gants de Jardinage'),
        (5, 'Gants de Ski'),
        (6, 'Gants de Protection')
    '''
    mycursor.execute(sql)

    # Création de la table commande
    sql = '''
    CREATE TABLE commande(
        id_commande INT,
        date_achat DATETIME,
        etat_id INT NOT NULL,
        utilisateur_id VARCHAR(50) NOT NULL,
        PRIMARY KEY(id_commande),
        FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
        FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    # Insertion des commandes
    sql = '''
    INSERT INTO commande VALUES
        (1, '2025-01-10 09:30:00', 2, 'U002'),
        (2, '2025-01-12 14:15:00', 2, 'U003'),
        (3, '2025-01-15 10:45:00', 1, 'U002'),
        (4, '2025-01-18 16:20:00', 1, 'U003'),
        (5, '2025-01-20 11:00:00', 2, 'U002'),
        (6, '2025-01-22 13:30:00', 1, 'U003'),
        (7, '2025-01-24 15:45:00', 2, 'U002')
    '''
    mycursor.execute(sql)

    # Création de la table gant
    sql = '''
    CREATE TABLE gant(
        id_gant INT,
        nom_gant VARCHAR(50),
        poids INT,
        couleur VARCHAR(50),
        prix_gant DECIMAL(19,4),
        photo VARCHAR(50),
        fournisseur VARCHAR(50),
        marque VARCHAR(50),
        stock INTEGER,
        type_gant_id INT NOT NULL,
        taille_id INT NOT NULL,
        PRIMARY KEY(id_gant),
        FOREIGN KEY(type_gant_id) REFERENCES type_gant(id_type_gant),
        FOREIGN KEY(taille_id) REFERENCES taille(id_taille)
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    # Insertion des gants
    sql = '''
    INSERT INTO gant VALUES
        (1, 'Specialized BG Grail', 85, 'Noir', 39.99, 'specialized_grail_noir.jpg', 'Sport 2000', 'Specialized', 4', 1, 5),
        (2, 'Specialized BG Grail', 85, 'Rouge', 39.99, 'specialized_grail_rouge.jpg', 'Sport 2000', 'Specialized', 38, 1, 7),
        (3, 'Giro DND Cycling', 75, 'Noir', 29.99, 'giro_dnd_noir.jpg', 'Sport 2000', 'Giro', 52, 1, 5),
        (4, 'Giro DND Cycling', 75, 'Vert', 29.99, 'giro_dnd_vert.jpg', 'Sport 2000', 'Giro', 30, 1, 7),
        (5, 'Specialized Prime-Series', 95, 'Bleu', 54.99, 'specialized_prime_bleu.jpg', 'Sport 2000', 'Specialized', 25, 1, 6),
        (6, 'Venum Elite Boxing 12oz', 420, 'Noir', 119.99, 'venum_elite_noir.jpg', 'Combat Sports France', 'Venum', 18, 2, 7),
        (7, 'Venum Elite Boxing 14oz', 450, 'Rouge', 119.99, 'venum_elite_rouge.jpg', 'Combat Sports France', 'Venum', 15, 2, 9),
        (8, 'Everlast PowerLock 12oz', 430, 'Noir', 89.99, 'everlast_power_noir.jpg', 'Combat Sports France', 'Everlast', 22, 2, 7),
        (9, 'Venum Impact MMA', 280, 'Noir', 69.99, 'venum_impact_noir.jpg', 'Combat Sports France', 'Venum', 35, 2, 5),
        (10, 'Everlast Pro Style 10oz', 380, 'Rouge', 44.99, 'everlast_pro_rouge.jpg', 'Combat Sports France', 'Everlast', 40, 2, 5),
        (11, 'The North Face Etip', 120, 'Noir', 49.99, 'tnf_etip_noir.jpg', 'Outdoor Adventure', 'The North Face', 55, 3, 5),
        (12, 'The North Face Etip', 120, 'Bleu', 49.99, 'tnf_etip_bleu.jpg', 'Outdoor Adventure', 'The North Face', 42, 3, 7),
        (13, 'Columbia Thermarator', 140, 'Noir', 34.99, 'columbia_therm_noir.jpg', 'Outdoor Adventure', 'Columbia', 65, 3, 5),
        (14, 'The North Face Montana', 180, 'Noir', 69.99, 'tnf_montana_noir.jpg', 'Outdoor Adventure', 'The North Face', 28, 3, 6),
        (15, 'Columbia Whirlibird', 160, 'Violet', 44.99, 'columbia_whirl_violet.jpg', 'Outdoor Adventure', 'Columbia', 35, 3, 5),
        (16, 'Rostaing Jardin Expert', 95, 'Vert', 14.99, 'rostaing_expert_vert.jpg', 'Jardin & Équipement Pro', 'Rostaing', 80, 4, 5),
        (17, 'Rostaing Jardin Expert', 95, 'Noir', 14.99, 'rostaing_expert_noir.jpg', 'Jardin & Équipement Pro', 'Rostaing', 75, 4, 7),
        (18, 'Mapa Jardin Pro', 110, 'Vert', 12.99, 'mapa_jardin_vert.jpg', 'Jardin & Équipement Pro', 'Mapa', 95, 4, 6),
        (19, 'Rostaing Rosier Premium', 85, 'Rose', 18.99, 'rostaing_rosier_rose.jpg', 'Jardin & Équipement Pro', 'Rostaing', 48, 4, 5),
        (20, 'Mechanix Garden Utility', 100, 'Vert', 24.99, 'mechanix_garden_vert.jpg', 'Jardin & Équipement Pro', 'Mechanix', 60, 4, 5),
        (21, 'Rossignol Ski Premium', 220, 'Noir', 79.99, 'rossignol_ski_noir.jpg', 'Mountain Gear Europe', 'Rossignol', 25, 5, 6),
        (22, 'The North Face Apex', 200, 'Blanc', 89.99, 'tnf_apex_blanc.jpg', 'Mountain Gear Europe', 'The North Face', 20, 5, 6),
        (23, 'Rossignol Tempest IMPR', 240, 'Rouge', 99.99, 'rossignol_tempest_rouge.jpg', 'Mountain Gear Europe', 'Rossignol', 18, 5, 7),
        (24, 'Mechanix Original', 130, 'Noir', 24.99, 'mechanix_orig_noir.jpg', 'Sport 2000', 'Mechanix', 70, 6, 5),
        (25, 'Mechanix M-Pact', 150, 'Rouge', 34.99, 'mechanix_mpact_rouge.jpg', 'Sport 2000', 'Mechanix', 55, 6, 6)
    '''
    mycursor.execute(sql)

    # Création de la table ligne_commande
    sql = '''
    CREATE TABLE ligne_commande(
        commande_id INT,
        gant_id INT,
        quantite INT,
        prix DECIMAL(19,4),
        PRIMARY KEY(commande_id, gant_id),
        FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
        FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    # Insertion des lignes de commande
    sql = '''
    INSERT INTO ligne_commande VALUES
        (1, 1, 1, 39.99),
        (1, 3, 2, 29.99),
        (2, 16, 3, 14.99),
        (2, 18, 2, 12.99),
        (3, 6, 1, 119.99),
        (3, 11, 1, 49.99),
        (4, 21, 1, 79.99),
        (4, 22, 1, 89.99),
        (5, 13, 2, 34.99),
        (5, 19, 1, 18.99),
        (6, 24, 2, 24.99),
        (6, 5, 1, 54.99),
        (7, 8, 1, 89.99),
        (7, 10, 1, 44.99)
    '''
    mycursor.execute(sql)

    # Création de la table ligne_panier
    sql = '''
    CREATE TABLE ligne_panier(
        utilisateur_id VARCHAR(50),
        gant_id INT,
        quantite INT,
        date_ajout DATE,
        PRIMARY KEY(utilisateur_id, gant_id),
        FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    # Insertion des lignes de panier
    sql = '''
    INSERT INTO ligne_panier VALUES
        ('U002', 7, 1, '2025-01-25'),
        ('U002', 14, 1, '2025-01-26'),
        ('U002', 20, 2, '2025-01-26'),
        ('U003', 2, 1, '2025-01-25'),
        ('U003', 9, 1, '2025-01-27'),
        ('U003', 23, 1, '2025-01-27')
    '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')