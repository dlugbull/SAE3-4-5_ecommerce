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
    sql = '''DROP TABLE IF EXISTS liste_envie'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS historique'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS commentaire'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS note'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS ligne_panier'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS ligne_commande'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS declinaison_gant'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS gant'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS commande'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS couleur'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS adresse'''
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
                                      id_utilisateur INT AUTO_INCREMENT,
                                      login VARCHAR(50),
                                      email VARCHAR(50),
                                      nom_utilisateur VARCHAR(50),
                                      password VARCHAR(255),
                                      role VARCHAR(50),
                                      PRIMARY KEY(id_utilisateur)
          ) DEFAULT CHARSET UTF8; \
          '''
    mycursor.execute(sql)

    # Insertion des utilisateurs
    sql = '''
          INSERT INTO utilisateur(login, email, nom_utilisateur, password, role) VALUES
                                                                                     ('admin', 'admin@example.com', 'Administrateur', 'pbkdf2:sha256:1000000$qwwvIJXyTvBTH4R1$73dd8f46cc5953965c9befed035509d47bb89b18166d02c2ee6b0924fb18f923', 'admin'),
                                                                                     ('client', 'client@example.com', 'Client Un', 'pbkdf2:sha256:1000000$9u2VVssEqRYwvrze$b3ef9670d06f24ed3dc11a92f1cca4c7b00dd5c301d13bbedec2d6f1f0bb6eb0', 'client'),
                                                                                     ('client2', 'client2@example.com', 'Client Deux', 'pbkdf2:sha256:1000000$Eq13PRiR0mkFGUej$4df2d53f486dc29e78c65a6ea3cc7004c4343bc58cdb8c91c19d43a3f84399fe', 'client'); \
          '''
    mycursor.execute(sql)

    # Création de la table etat
    sql = '''
          CREATE TABLE etat(
                               id_etat INT AUTO_INCREMENT,
                               libelle_etat VARCHAR(50),
                               PRIMARY KEY(id_etat)
          ) DEFAULT CHARSET UTF8; \
          '''
    mycursor.execute(sql)

    # Insertion des états
    sql = '''
          INSERT INTO etat(libelle_etat) VALUES
                                             ('En état'),
                                             ('Expédiée');
          '''
    mycursor.execute(sql)

    # Création de la table taille
    sql = '''
          CREATE TABLE taille(
                                 id_taille INT AUTO_INCREMENT,
                                 num_taille_fr VARCHAR(50),
                                 taille_us VARCHAR(50),
                                 tour_de_main VARCHAR(50),
                                 PRIMARY KEY(id_taille)
          ) DEFAULT CHARSET UTF8; \
          '''
    mycursor.execute(sql)

    # Insertion des tailles
    sql = '''
          INSERT INTO taille(num_taille_fr, taille_us, tour_de_main) VALUES
                                                                         ('Taille unique', 'One size', 'Ajustable'),
                                                                         ('7', 'S', '17 cm'),
                                                                         ('8', 'M', '19 cm'),
                                                                         ('9', 'L', '21 cm'),
                                                                         ('10', 'XL', '23 cm');
          '''
    mycursor.execute(sql)

    # Création de la table type_gant
    sql = '''
          CREATE TABLE type_gant(
                                    id_type_gant INT AUTO_INCREMENT,
                                    nom_type_gant VARCHAR(255),
                                    PRIMARY KEY(id_type_gant)
          ) DEFAULT CHARSET UTF8; \
          '''
    mycursor.execute(sql)

    # Insertion des types de gants
    sql = '''
          INSERT INTO type_gant(nom_type_gant) VALUES
                                                   ('Boxe'),
                                                   ('Jardinage'),
                                                   ('Cyclisme'),
                                                   ('Ski'),
                                                   ('Travail'),
                                                   ('Randonnée');
          '''
    mycursor.execute(sql)

    # Création de la table adresse
    sql='''
        CREATE TABLE adresse(
                                id_adresse INT AUTO_INCREMENT,
                                nom_adresse VARCHAR(50),
                                rue VARCHAR(50),
                                code_postal VARCHAR(50),
                                ville VARCHAR(50),
                                date_utilisation DATE,
                                utilisateur_id INT NOT NULL,
                                PRIMARY KEY(id_adresse),
                                FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
        ) DEFAULT CHARSET UTF8; \
        '''
    mycursor.execute(sql)

    # Insertion des adresses
    sql='''
        INSERT INTO adresse(nom_adresse, rue, code_postal, ville, date_utilisation, utilisateur_id) VALUES
                                                                                                        ('Maison',  '1 rue du Centre',        '25000', 'Besançon',    '2024-01-01', 2),
                                                                                                        ('Travail', '12 avenue Victor Hugo',  '25000', 'Besançon',    '2024-02-01', 2),
                                                                                                        ('Maison',  '5 rue des Lilas',        '25200', 'Montbéliard', '2024-03-01', 3),
                                                                                                        ('Parents', '8 rue de la République', '25300', 'Pontarlier',  '2024-03-15', 3); \
        '''
    mycursor.execute(sql)

    # Création de la table couleur
    sql='''
        CREATE TABLE couleur(
                                id_couleur INT AUTO_INCREMENT,
                                libelle_couleur VARCHAR(50),
                                code_couleur VARCHAR(255),
                                PRIMARY KEY(id_couleur)
        ) DEFAULT CHARSET UTF8; \
        '''
    mycursor.execute(sql)

    # Insertion dans la table couleur
    sql='''
        INSERT INTO couleur(libelle_couleur, code_couleur) VALUES
                                                               ('Couleur unique', 'black'),
                                                               ('Noir', 'black'),
                                                               ('Bleu', 'blue'),
                                                               ('Rouge', 'red'),
                                                               ('Gris', 'grey'),
                                                               ('Vert', 'green'),
                                                               ('Jaune', 'yellow'),
                                                               ('Blanc', 'white'),
                                                               ('Orange','orange');
        '''
    mycursor.execute(sql)

    # Création de la table commande
    sql = '''
          CREATE TABLE commande(
                                   id_commande INT AUTO_INCREMENT,
                                   date_achat DATETIME,
                                   etat_id INT NOT NULL,
                                   utilisateur_id INT NOT NULL,
                                   adresse_id_livre INT NOT NULL,
                                   adresse_id_fact INT NOT NULL,
                                   PRIMARY KEY(id_commande),
                                   FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
                                   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                                   FOREIGN KEY(adresse_id_livre) REFERENCES adresse(id_adresse),
                                   FOREIGN KEY(adresse_id_fact) REFERENCES adresse(id_adresse)
          ) DEFAULT CHARSET UTF8; \
          '''
    mycursor.execute(sql)

    # Insertion des commandes
    sql = '''
          INSERT INTO commande(date_achat, etat_id, utilisateur_id, adresse_id_livre, adresse_id_fact) VALUES
                                                                                                           ('2024-04-01 10:00:00', 1, 2, 1, 2),  -- id 1 : client, livraison Maison, fact Travail
                                                                                                           ('2024-04-05 15:30:00', 2, 3, 3, 3),  -- id 2 : client2, expédiée
                                                                                                           ('2024-04-20 09:15:00', 1, 2, 1, 2),  -- id 3 : client, en attente
                                                                                                           ('2024-05-03 14:00:00', 2, 3, 4, 4);  -- id 4 : client2, expédiée \
          '''
    mycursor.execute(sql)

    # Création de la table gant
    sql = '''
          CREATE TABLE gant(
                               id_gant INT AUTO_INCREMENT,
                               nom_gant VARCHAR(50),
                               poids INT,
                               prix_gant DECIMAL(15,2),
                               photo VARCHAR(50),
                               fournisseur VARCHAR(50),
                               marque VARCHAR(50),
                               description VARCHAR(255),
                               type_gant_id INT NOT NULL,
                               PRIMARY KEY(id_gant),
                               FOREIGN KEY(type_gant_id) REFERENCES type_gant(id_type_gant)
          ) DEFAULT CHARSET UTF8; \
          '''
    mycursor.execute(sql)

    # Insertion des gants (25 gants)
    sql = '''
          INSERT INTO gant(nom_gant, poids, prix_gant, photo, fournisseur, marque, description, type_gant_id) VALUES
-- Boxe (type 1)
('Adidas Speed Bleu',   300, 59.99,  'adidas_speed_bleu.jpg',            'Adidas',         'Adidas',    'Gants de boxe rapides et légers',         1),  -- id 1
('Everlast Powerlock',  320, 79.99,  'everlast_powerlock.jpg',           'Everlast',       'Everlast',  'Gants de boxe Powerlock',                 1),  -- id 2
('Venum Impact',        330, 89.99,  'venum_impact.jpg',                 'Venum',          'Venum',     'Gants de boxe Impact polyvalents',        1),  -- id 3
('Everlast Prostyle',   310, 69.99,  'everlast_prostyle.jpg',            'Everlast',       'Everlast',  'Gants de boxe Prostyle entrainement',     1),  -- id 4
('Venum Elite',         350, 99.99,  'venum_elite.jpg',                  'Venum',          'Venum',     'Gants de boxe Elite compétition',         1),  -- id 5
-- Jardinage (type 2)
('Mechanix Garden',     150, 19.99,  'mechanix_garden.jpg',              'Mechanix',       'Mechanix',  'Gants de jardinage résistants',           2),  -- id 6
('Rostaing Expert',     160, 22.99,  'rostaing_expert.jpg',              'Rostaing',       'Rostaing',  'Gants de jardinage expert',               2),  -- id 7
('Rostaing Rosier',     150, 17.99,  'rostaing_rosier.jpg',              'Rostaing',       'Rostaing',  'Gants spéciaux rosiers anti-épines',      2),  -- id 8
('Mapa Jardin',         110,  9.99,  'mapa_jardin.jpg',                  'Mapa',           'Mapa',      'Gants de jardinage classiques',           2),  -- id 9
-- Cyclisme (type 3)
('Specialized Prime',   120, 34.99,  'specialized_prime.jpg',            'Specialized',    'Specialized','Gants vélo Prime demi-doigts',           3),  -- id 10
('Giro DND',            140, 29.99,  'giro_dnd.jpg',                     'Giro',           'Giro',      'Gants vélo DND tout-terrain',             3),  -- id 11
('Triban RC500 Noir',   130, 24.99,  'triban_rc500_noir.jpg',            'Triban',         'Triban',    'Gants vélo RC500 route',                  3),  -- id 12
('Specialized Grail',   125, 32.99,  'specialized_grail.jpg',            'Specialized',    'Specialized','Gants vélo Grail longs doigts',          3),  -- id 13
('Fox Ranger Gris',     150, 29.99,  'fox_ranger_gris.jpg',              'Fox',            'Fox',       'Gants vélo Ranger VTT',                   3),  -- id 14
-- Ski (type 4)
('Rossignol Noir',      200, 49.99,  'gant_type_impr_rossignol_noir.jpg','Rossignol',      'Rossignol', 'Gants de ski imprimés Rossignol',         4),  -- id 15
('Rossignol Ski',       260, 79.99,  'rossignol_ski.jpg',                'Rossignol',      'Rossignol', 'Gants de ski Rossignol haute performance', 4), -- id 16
-- Travail (type 5)
('Milwaukee Cut5 Gris', 180, 24.99,  'milwaukee_cut5_gris.jpg',          'Milwaukee',      'Milwaukee', 'Gants anti-coupure niveau 5',             5),  -- id 17
('Mechanix Mpact',      190, 27.99,  'mechanix_mpact.jpg',               'Mechanix',       'Mechanix',  'Gants de travail Mpact anti-impact',      5),  -- id 18
('Mechanix Original',   180, 25.99,  'mechanix_original.jpg',            'Mechanix',       'Mechanix',  'Gants de travail Original multi-usage',   5),  -- id 19
-- Randonnée (type 6)
('TNF Montana',         250, 69.99,  'tnf_montana.jpg',                  'The North Face', 'TNF',       'Gants chauds Montana grand froid',        6),  -- id 20
('Columbia Therma',     210, 54.99,  'columbia_therma.jpg',              'Columbia',       'Columbia',  'Gants thermiques Columbia hiver',         6),  -- id 21
('TNF Apex',            240, 74.99,  'tnf_apex.jpg',                     'The North Face', 'TNF',       'Gants Apex softshell imperméables',       6),  -- id 22
('Quechua SH500 Noir',  230, 39.99,  'quechua_sh500_noir.jpg',           'Quechua',        'Quechua',   'Gants hiver SH500 imperméables',          6),  -- id 23
('Columbia Whirli',     220, 49.99,  'columbia_whirli.jpg',              'Columbia',       'Columbia',  'Gants Whirlibird convertibles',           6),  -- id 24
('TNF Etip',            140, 44.99,  'tnf_etip.jpg',                     'The North Face', 'TNF',       'Gants tactiles Etip connectivité',        6);  -- id 25 \
          '''
    mycursor.execute(sql)

    # Création de la table declinaison_gant
    sql='''
        CREATE TABLE declinaison_gant(
                                         id_declinaison_gant INT AUTO_INCREMENT,
                                         stock INT,
                                         prix_declinaison DECIMAL(15, 2),
                                         image VARCHAR(50),
                                         taille_id INT NOT NULL,
                                         couleur_id INT NOT NULL,
                                         gant_id INT NOT NULL,
                                         PRIMARY KEY(id_declinaison_gant),
                                         FOREIGN KEY(taille_id) REFERENCES taille(id_taille),
                                         FOREIGN KEY(couleur_id) REFERENCES couleur(id_couleur),
                                         FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
        ) DEFAULT CHARSET UTF8; \
        '''
    mycursor.execute(sql)

    # Insertion des déclinaisons de gants
    sql='''
        INSERT INTO declinaison_gant(stock, prix_declinaison, image, taille_id, couleur_id, gant_id) VALUES
                                                                                                         (15, 62.99, NULL, 2, 3, 1), (20, 62.99, NULL, 3, 3, 1), (18, 64.99, NULL, 4, 3, 1),
                                                                                                         (10, 67.99, NULL, 5, 3, 1), (12, 59.99, NULL, 2, 2, 1), (16, 59.99, NULL, 3, 2, 1),
                                                                                                         (14, 61.99, NULL, 4, 2, 1), (8,  64.99, NULL, 5, 2, 1), (20, 79.99, NULL, 2, 2, 2),
                                                                                                         (25, 79.99, NULL, 3, 2, 2), (22, 81.99, NULL, 4, 2, 2), (12, 84.99, NULL, 5, 2, 2),
                                                                                                         (18, 82.99, NULL, 2, 4, 2), (20, 82.99, NULL, 3, 4, 2), (15, 84.99, NULL, 4, 4, 2),
                                                                                                         (8,  87.99, NULL, 5, 4, 2), (14, 89.99, NULL, 2, 2, 3), (18, 89.99, NULL, 3, 2, 3),
                                                                                                         (16, 91.99, NULL, 4, 2, 3), (12, 92.99, NULL, 2, 3, 3), (16, 92.99, NULL, 3, 3, 3),
                                                                                                         (10, 94.99, NULL, 4, 3, 3), (16, 69.99, NULL, 2, 2, 4), (20, 69.99, NULL, 3, 2, 4),
                                                                                                         (18, 71.99, NULL, 4, 2, 4), (10, 74.99, NULL, 5, 2, 4), (14, 72.99, NULL, 2, 3, 4),
                                                                                                         (18, 72.99, NULL, 3, 3, 4), (15, 74.99, NULL, 4, 3, 4), (8,  77.99, NULL, 5, 3, 4),
                                                                                                         (10, 99.99, NULL, 2, 2, 5), (15, 99.99, NULL, 3, 2, 5), (12, 101.99, NULL, 4, 2, 5),
                                                                                                         (6,  104.99, NULL, 5, 2, 5), (8,  102.99, NULL, 2, 4, 5), (12, 102.99, NULL, 3, 4, 5),
                                                                                                         (10, 104.99, NULL, 4, 4, 5), (5,  107.99, NULL, 5, 4, 5), (35, 19.99, NULL, 1, 6, 6),
                                                                                                         (30, 22.99, NULL, 1, 3, 6), (40, 22.99, NULL, 1, 6, 7), (50, 17.99, NULL, 1, 1, 8),
                                                                                                         (60, 9.99, NULL, 1, 6, 9), (55, 14.99, NULL, 1, 7, 9), (18, 37.99, NULL, 2, 3, 10),
                                                                                                         (22, 37.99, NULL, 3, 3, 10), (15, 39.99, NULL, 4, 3, 10), (16, 34.99, NULL, 2, 2, 10),
                                                                                                         (20, 34.99, NULL, 3, 2, 10), (12, 36.99, NULL, 4, 2, 10), (20, 29.99, NULL, 2, 2, 11),
                                                                                                         (24, 29.99, NULL, 3, 2, 11), (18, 31.99, NULL, 4, 2, 11), (15, 29.99, NULL, 2, 5, 11),
                                                                                                         (20, 29.99, NULL, 3, 5, 11), (14, 31.99, NULL, 4, 5, 11), (25, 24.99, NULL, 2, 2, 12),
                                                                                                         (30, 24.99, NULL, 3, 2, 12), (22, 26.99, NULL, 4, 2, 12), (12, 32.99, NULL, 2, 2, 13),
                                                                                                         (16, 32.99, NULL, 3, 2, 13), (14, 34.99, NULL, 4, 2, 13), (10, 35.99, NULL, 2, 3, 13),
                                                                                                         (14, 35.99, NULL, 3, 3, 13), (12, 37.99, NULL, 4, 3, 13), (18, 29.99, NULL, 2, 5, 14),
                                                                                                         (22, 29.99, NULL, 3, 5, 14), (16, 31.99, NULL, 4, 5, 14), (15, 34.99, NULL, 2, 9, 14),
                                                                                                         (18, 34.99, NULL, 3, 9, 14), (12, 36.99, NULL, 4, 9, 14), (12, 49.99, NULL, 2, 2, 15),
                                                                                                         (16, 49.99, NULL, 3, 2, 15), (14, 51.99, NULL, 4, 2, 15), (8,  54.99, NULL, 5, 2, 15),
                                                                                                         (10, 52.99, NULL, 2, 3, 15), (14, 52.99, NULL, 3, 3, 15), (12, 54.99, NULL, 4, 3, 15),
                                                                                                         (6,  57.99, NULL, 5, 3, 15), (10, 79.99, NULL, 2, 2, 16), (14, 79.99, NULL, 3, 2, 16),
                                                                                                         (12, 81.99, NULL, 4, 2, 16), (6,  84.99, NULL, 5, 2, 16), (8,  82.99, NULL, 2, 4, 16),
                                                                                                         (12, 82.99, NULL, 3, 4, 16), (10, 84.99, NULL, 4, 4, 16), (5,  87.99, NULL, 5, 4, 16),
                                                                                                         (20, 24.99, NULL, 2, 5, 17), (25, 24.99, NULL, 3, 5, 17), (22, 26.99, NULL, 4, 5, 17),
                                                                                                         (15, 29.99, NULL, 5, 5, 17), (18, 29.99, NULL, 2, 9, 17), (22, 29.99, NULL, 3, 9, 17),
                                                                                                         (20, 31.99, NULL, 4, 9, 17), (12, 34.99, NULL, 5, 9, 17), (18, 27.99, NULL, 2, 2, 18),
                                                                                                         (22, 27.99, NULL, 3, 2, 18), (20, 29.99, NULL, 4, 2, 18), (14, 32.99, NULL, 5, 2, 18),
                                                                                                         (16, 27.99, NULL, 2, 5, 18), (20, 27.99, NULL, 3, 5, 18), (18, 29.99, NULL, 4, 5, 18),
                                                                                                         (10, 32.99, NULL, 5, 5, 18), (25, 25.99, NULL, 2, 2, 19), (30, 25.99, NULL, 3, 2, 19),
                                                                                                         (28, 27.99, NULL, 4, 2, 19), (18, 30.99, NULL, 5, 2, 19), (12, 69.99, NULL, 2, 2, 20),
                                                                                                         (16, 69.99, NULL, 3, 2, 20), (14, 71.99, NULL, 4, 2, 20), (8,  74.99, NULL, 5, 2, 20),
                                                                                                         (10, 72.99, NULL, 2, 3, 20), (14, 72.99, NULL, 3, 3, 20), (12, 74.99, NULL, 4, 3, 20),
                                                                                                         (6,  77.99, NULL, 5, 3, 20), (14, 54.99, NULL, 2, 2, 21), (18, 54.99, NULL, 3, 2, 21),
                                                                                                         (16, 56.99, NULL, 4, 2, 21), (10, 59.99, NULL, 5, 2, 21), (12, 57.99, NULL, 2, 4, 21),
                                                                                                         (16, 57.99, NULL, 3, 4, 21), (14, 59.99, NULL, 4, 4, 21), (8,  62.99, NULL, 5, 4, 21),
                                                                                                         (10, 74.99, NULL, 2, 2, 22), (14, 74.99, NULL, 3, 2, 22), (12, 76.99, NULL, 4, 2, 22),
                                                                                                         (6,  79.99, NULL, 5, 2, 22), (8,  74.99, NULL, 2, 5, 22), (12, 74.99, NULL, 3, 5, 22),
                                                                                                         (10, 76.99, NULL, 4, 5, 22), (5,  79.99, NULL, 5, 5, 22), (20, 39.99, NULL, 2, 2, 23),
                                                                                                         (25, 39.99, NULL, 3, 2, 23), (22, 41.99, NULL, 4, 2, 23), (15, 44.99, NULL, 5, 2, 23),
                                                                                                         (12, 49.99, NULL, 2, 2, 24), (16, 49.99, NULL, 3, 2, 24), (14, 51.99, NULL, 4, 2, 24),
                                                                                                         (8,  54.99, NULL, 5, 2, 24), (10, 52.99, NULL, 2, 3, 24), (14, 52.99, NULL, 3, 3, 24),
                                                                                                         (12, 54.99, NULL, 4, 3, 24), (6,  57.99, NULL, 5, 3, 24), (14, 44.99, NULL, 2, 2, 25),
                                                                                                         (18, 44.99, NULL, 3, 2, 25), (16, 46.99, NULL, 4, 2, 25), (10, 49.99, NULL, 5, 2, 25),
                                                                                                         (12, 44.99, NULL, 2, 5, 25), (16, 44.99, NULL, 3, 5, 25), (14, 46.99, NULL, 4, 5, 25),
                                                                                                         (8,  49.99, NULL, 5, 5, 25); \
        '''
    mycursor.execute(sql)


    # Création de la table ligne_commande
    sql = '''
          CREATE TABLE ligne_commande(
                                         commande_id INT,
                                         declinaison_gant_id INT,
                                         quantite INT,
                                         prix DECIMAL(19,2),
                                         PRIMARY KEY(commande_id, declinaison_gant_id),
                                         FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
                                         FOREIGN KEY(declinaison_gant_id) REFERENCES declinaison_gant(id_declinaison_gant)
          ) DEFAULT CHARSET UTF8; \
          '''
    mycursor.execute(sql)

    # Insertion des lignes de commande
    sql = '''
          INSERT INTO ligne_commande VALUES
                                         (1, 2,  2, 59.99),   -- commande 1 : Adidas Speed Bleu M/Bleu, qté 2
                                         (1, 24, 1, 69.99),   -- commande 1 : Everlast Prostyle M/Noir, qté 1
                                         (2, 89, 2, 24.99),   -- commande 2 : Milwaukee Cut5 M/Gris, qté 2
                                         (2, 58, 1, 24.99),   -- commande 2 : Triban RC500 M/Noir, qté 1
                                         (3, 117,1, 54.99),   -- commande 3 : Columbia Therma M/Noir, qté 1
                                         (3, 33, 1, 99.99),   -- commande 3 : Venum Elite L/Noir, qté 1
                                         (4, 113,2, 69.99),   -- commande 4 : TNF Montana M/Bleu, qté 2
                                         (4, 89, 3, 24.99);   -- commande 4 : Milwaukee Cut5 M/Gris, qté 3 \
          '''
    mycursor.execute(sql)

    # Création de la table ligne_panier
    sql = '''
          CREATE TABLE ligne_panier(
                                       utilisateur_id INT,
                                       declinaison_gant_id INT,
                                       quantite INT,
                                       date_ajout DATE,
                                       PRIMARY KEY(utilisateur_id, declinaison_gant_id),
                                       FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                                       FOREIGN KEY(declinaison_gant_id) REFERENCES declinaison_gant(id_declinaison_gant)
          ) DEFAULT CHARSET UTF8;
          '''
    mycursor.execute(sql)

    # Insertion des lignes de panier
    sql = '''
          INSERT INTO ligne_panier VALUES
                                       (2, 36,  1, '2024-04-10'),  -- client : Venum Elite M/Rouge
                                       (2, 125, 1, '2024-04-11'),  -- client : TNF Apex M/Noir
                                       (3, 46,  2, '2024-04-12'),  -- client2 : Specialized Prime M/Bleu
                                       (3, 67,  1, '2024-04-14');  -- client2 : Fox Ranger M/Gris \
          '''
    mycursor.execute(sql)

    # Création de la table note
    sql='''
        CREATE TABLE note(
                             utilisateur_id INT,
                             gant_id INT,
                             note INT,
                             PRIMARY KEY(utilisateur_id, gant_id),
                             FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                             FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
        ) DEFAULT CHARSET UTF8; \
        '''
    mycursor.execute(sql)

    # Insertion des notes
    sql='''
        INSERT INTO note VALUES
                             (2, 1,  5),   -- client note Adidas Speed Bleu : 5/5
                             (2, 4,  4),   -- client note Everlast Prostyle : 4/5
                             (2, 10, 5),   -- client note Specialized Prime : 5/5
                             (3, 12, 4),   -- client2 note Triban RC500 : 4/5
                             (3, 17, 5),   -- client2 note Milwaukee Cut5 : 5/5
                             (3, 21, 3);   -- client2 note Columbia Therma : 3/5 \
        '''
    mycursor.execute(sql)

    # Création de la table commentaire
    sql='''
        CREATE TABLE commentaire(
                                    utilisateur_id INT,
                                    gant_id INT,
                                    date_publication DATETIME,
                                    commentaire VARCHAR(50),
                                    valider BOOLEAN,
                                    PRIMARY KEY(utilisateur_id, gant_id, date_publication),
                                    FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                                    FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
        ) DEFAULT CHARSET UTF8; \
        '''
    mycursor.execute(sql)

    # Insertion des commentaires
    sql='''
        INSERT INTO commentaire VALUES
                                    (2, 1,  '2024-04-12 10:00:00', 'Très bons gants de boxe',  TRUE),
                                    (2, 4,  '2024-04-15 11:00:00', 'Bon rapport qualité prix', TRUE),
                                    (2, 10, '2024-04-18 12:00:00', 'Parfaits pour le vélo',    TRUE),
                                    (3, 12, '2024-04-20 09:00:00', 'Légers et confortables',   TRUE),
                                    (3, 17, '2024-04-22 14:00:00', 'Très bonne protection',    FALSE),
                                    (3, 21, '2024-04-25 16:00:00', 'Corrects mais un peu fins', TRUE); \
        '''
    mycursor.execute(sql)

    # Création de la table historique
    sql='''
        CREATE TABLE historique(
                                   utilisateur_id INT,
                                   gant_id INT,
                                   date_consultation DATE,
                                   PRIMARY KEY(utilisateur_id, gant_id, date_consultation),
                                   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                                   FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
        ) DEFAULT CHARSET UTF8; \
        '''
    mycursor.execute(sql)

    # Insertion des historiques
    sql='''
        INSERT INTO historique VALUES
                                   (2, 1,  '2024-04-01'),
                                   (2, 3,  '2024-04-02'),
                                   (2, 5,  '2024-04-03'),
                                   (2, 10, '2024-04-05'),
                                   (2, 22, '2024-04-06'),
                                   (3, 12, '2024-04-03'),
                                   (3, 14, '2024-04-04'),
                                   (3, 17, '2024-04-05'),
                                   (3, 20, '2024-04-06'),
                                   (3, 25, '2024-04-07'); \
        '''
    mycursor.execute(sql)

    # Création de la table liste_envie
    sql='''
        CREATE TABLE liste_envie(
                                    utilisateur_id INT,
                                    gant_id INT,
                                    date_update DATE,
                                    PRIMARY KEY(utilisateur_id, gant_id, date_update),
                                    FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                                    FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
        ) DEFAULT CHARSET UTF8; \
        '''
    mycursor.execute(sql)

    # Insertion des listes d'envies
    sql='''
        INSERT INTO liste_envie VALUES
                                    (2, 5,  '2024-04-15'),  -- client veut Venum Elite
                                    (2, 22, '2024-04-16'),  -- client veut TNF Apex
                                    (2, 16, '2024-04-17'),  -- client veut Rossignol Ski
                                    (3, 1,  '2024-04-15'),  -- client2 veut Adidas Speed Bleu
                                    (3, 25, '2024-04-16'),  -- client2 veut TNF Etip
                                    (3, 10, '2024-04-18');  -- client2 veut Specialized Prime
        '''
    mycursor.execute(sql)

    get_db().commit()
    mycursor.close()
    return redirect('/')
