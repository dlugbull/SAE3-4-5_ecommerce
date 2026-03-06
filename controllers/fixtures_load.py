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
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des utilisateurs
    sql = '''
    INSERT INTO utilisateur VALUES
        (1, 'admin', 'admin@boutique-gants.fr', 'Administrateur', 'pbkdf2:sha256:1000000$qwwvIJXyTvBTH4R1$73dd8f46cc5953965c9befed035509d47bb89b18166d02c2ee6b0924fb18f923', 'admin'),
        (2, 'client', 'client@email.com', 'Sophie Martin', 'pbkdf2:sha256:1000000$9u2VVssEqRYwvrze$b3ef9670d06f24ed3dc11a92f1cca4c7b00dd5c301d13bbedec2d6f1f0bb6eb0', 'client'),
        (3, 'client2', 'client2@email.com', 'Thomas Dubois', 'pbkdf2:sha256:1000000$Eq13PRiR0mkFGUej$4df2d53f486dc29e78c65a6ea3cc7004c4343bc58cdb8c91c19d43a3f84399fe', 'client');

    '''
    mycursor.execute(sql)

    # Création de la table etat
    sql = '''
    CREATE TABLE etat(
        id_etat INT AUTO_INCREMENT,
        libelle_etat VARCHAR(50),
        PRIMARY KEY(id_etat)
    ) DEFAULT CHARSET=utf8
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
        id_taille INT AUTO_INCREMENT,
        num_taille_fr VARCHAR(50),
        taille_us VARCHAR(50),
        tour_de_main VARCHAR(50),
        PRIMARY KEY(id_taille)
    ) DEFAULT CHARSET=utf8
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
        id_type_gant INT AUTO_INCREMENT,
        nom_type_gant VARCHAR(255),
        PRIMARY KEY(id_type_gant)
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des types de gants
    sql = '''
    INSERT INTO type_gant VALUES
        (1, 'Gants de Vélo'),
        (2, 'Gants de Sport Combat'),
        (3, 'Gants d\\'Hiver'),
        (4, 'Gants de Jardinage'),
        (5, 'Gants de Ski'),
        (6, 'Gants de Protection')
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
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des adresses
    sql='''
    INSERT INTO adresse VALUES
        -- Adresses de Sophie Martin (client)
        (1, 'Domicile', '12 rue des Lilas', '75015', 'Paris', '2025-01-10', 2),
        (2, 'Bureau', '45 avenue Montaigne', '75008', 'Paris', '2025-01-15', 2),
        -- Adresses de Thomas Dubois (client2)
        (3, 'Maison', '78 boulevard Victor Hugo', '69003', 'Lyon', '2025-01-12', 3),
        (4, 'Travail', '23 rue de la République', '69002', 'Lyon', '2025-01-18', 3);
    '''
    mycursor.execute(sql)

    # Création de la table commande
    sql = '''
    CREATE TABLE commande(
        id_commande INT AUTO_INCREMENT,
        date_achat DATETIME,
        etat_id INT NOT NULL,
        utilisateur_id INT NOT NULL,
        adresse_id_fact INT NOT NULL,
        adresse_id_livre INT NOT NULL,
        PRIMARY KEY(id_commande),
        FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
        FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY(adresse_id_livre) REFERENCES adresse(id_adresse),
        FOREIGN KEY(adresse_id_fact) REFERENCES adresse(id_adresse)
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des commandes
    sql = '''
    INSERT INTO commande VALUES
        (1, '2025-01-10 09:30:00', 2, 2, 1, 1),
        (2, '2025-01-12 14:15:00', 2, 3, 3, 3),
        (3, '2025-01-15 10:45:00', 1, 2, 1, 2),
        (4, '2025-01-18 16:20:00', 1, 3, 4, 3),
        (5, '2025-01-20 11:00:00', 2, 2, 2, 2),
        (6, '2025-01-22 13:30:00', 1, 3, 3, 4),
        (7, '2025-01-24 15:45:00', 2, 2, 1, 1);
    '''
    mycursor.execute(sql)

    # Création de la table gant
    sql = '''
    CREATE TABLE gant(
        id_gant INT AUTO_INCREMENT,
        nom_gant VARCHAR(50),
        poids INT,
        couleur VARCHAR(50),
        prix_gant DECIMAL(19,2),
        photo VARCHAR(50),
        fournisseur VARCHAR(50),
        marque VARCHAR(50),
        description VARCHAR(255),
        type_gant_id INT NOT NULL,
        PRIMARY KEY(id_gant),
        FOREIGN KEY(type_gant_id) REFERENCES type_gant(id_type_gant)
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des gants (25 gants)
    sql = '''
    INSERT INTO gant VALUES
        -- Gants de Vélo (5 modèles)
        (1, 'Specialized BG Grail', 85, 'Noir/Rouge', 39.99, 'specialized_grail.jpg', 'Sport 2000', 'Specialized', 'Gants de vélo haute performance avec rembourrage gel', 1),
        (2, 'Giro DND Cycling', 75, 'Noir/Jaune', 29.99, 'giro_dnd.jpg', 'Sport 2000', 'Giro', 'Gants de cyclisme respirants et confortables', 1),
        (3, 'Specialized Prime-Series', 95, 'Bleu/Noir', 54.99, 'specialized_prime.jpg', 'Sport 2000', 'Specialized', 'Gants premium pour cyclisme longue distance', 1),
        (4, 'Decathlon Triban RC500', 90, 'Noir', 19.99, 'triban_rc500_noir.jpg', 'Decathlon', 'Triban', 'Gants de route légers et ventilés', 1),
        (5, 'Fox Ranger Gel', 105, 'Gris', 34.99, 'fox_ranger_gris.jpg', 'Sport 2000', 'Fox', 'Gants VTT avec protection et grip renforcé', 1),
    
        -- Gants de Sport Combat (5 modèles)
        (6, 'Venum Elite Boxing', 420, 'Blanc/Or', 119.99, 'venum_elite.jpg', 'Combat Sports France', 'Venum', 'Gants de boxe professionnels en cuir premium', 2),
        (7, 'Everlast PowerLock', 430, 'Rouge/Noir', 89.99, 'everlast_powerlock.jpg', 'Combat Sports France', 'Everlast', 'Gants d entraînement avec système PowerLock', 2),
        (8, 'Venum Impact MMA', 280, 'Noir/Rouge', 69.99, 'venum_impact.jpg', 'Combat Sports France', 'Venum', 'Gants MMA polyvalents pour sparring', 2),
        (9, 'Everlast Pro Style', 380, 'Rouge', 44.99, 'everlast_prostyle.jpg', 'Combat Sports France', 'Everlast', 'Gants de boxe style professionnel', 2),
        (10, 'Adidas Speed 50', 400, 'Bleu/Blanc', 79.99, 'adidas_speed_bleu.jpg', 'Combat Sports France', 'Adidas', 'Gants de compétition légers et rapides', 2),
    
        -- Gants d'Hiver (5 modèles)
        (11, 'The North Face Etip', 120, 'Noir', 49.99, 'tnf_etip.jpg', 'Outdoor Adventure', 'The North Face', 'Gants tactiles pour écrans avec isolation thermique', 3),
        (12, 'Columbia Thermarator', 140, 'Noir/Gris', 34.99, 'columbia_therma.jpg', 'Outdoor Adventure', 'Columbia', 'Gants chauds et imperméables pour l hiver', 3),
        (13, 'The North Face Montana', 180, 'Noir', 69.99, 'tnf_montana.jpg', 'Outdoor Adventure', 'The North Face', 'Gants d hiver premium avec isolation Gore-Tex', 3),
        (14, 'Columbia Whirlibird', 160, 'Violet/Noir', 44.99, 'columbia_whirli.jpg', 'Outdoor Adventure', 'Columbia', 'Gants polyvalents pour sports d hiver', 3),
        (15, 'Quechua SH500', 150, 'Noir', 24.99, 'quechua_sh500_noir.jpg', 'Decathlon', 'Quechua', 'Gants de randonnée hivernale chauds', 3),
    
        -- Gants de Jardinage (4 modèles)
        (16, 'Rostaing Jardin Expert', 95, 'Vert/Noir', 14.99, 'rostaing_expert.jpg', 'Jardin & Équipement Pro', 'Rostaing', 'Gants de jardinage résistants aux épines', 4),
        (17, 'Mapa Jardin Pro', 110, 'Vert/Jaune', 12.99, 'mapa_jardin.jpg', 'Jardin & Équipement Pro', 'Mapa', 'Gants imperméables pour travaux de jardinage', 4),
        (18, 'Rostaing Rosier Premium', 85, 'Rose/Blanc', 18.99, 'rostaing_rosier.jpg', 'Jardin & Équipement Pro', 'Rostaing', 'Gants spécial rosiers ultra-résistants', 4),
        (19, 'Mechanix Garden Utility', 100, 'Vert/Noir', 24.99, 'mechanix_garden.jpg', 'Jardin & Équipement Pro', 'Mechanix', 'Gants de jardinage techniques et durables', 4),
    
        -- Gants de Ski (3 modèles)
        (20, 'Rossignol Ski Premium', 220, 'Noir/Jaune', 79.99, 'rossignol_ski.jpg', 'Mountain Gear Europe', 'Rossignol', 'Gants de ski haute performance avec isolation', 5),
        (21, 'The North Face Apex', 200, 'Noir/Gris', 89.99, 'tnf_apex.jpg', 'Mountain Gear Europe', 'The North Face', 'Gants de ski imperméables et respirants', 5),
        (22, 'Rossignol Tempest IMPR', 240, 'Noir/Rouge', 99.99, 'gant_type_impr_rossignol_noir.jpg', 'Mountain Gear Europe', 'Rossignol', 'Gants de ski freeride avec protection renforcée', 5),
    
        -- Gants de Protection (3 modèles)
        (23, 'Mechanix Original', 130, 'Noir', 24.99, 'mechanix_original.jpg', 'Sport 2000', 'Mechanix', 'Gants de protection polyvalents et résistants', 6),
        (24, 'Mechanix M-Pact', 150, 'Noir/Rouge', 34.99, 'mechanix_mpact.jpg', 'Sport 2000', 'Mechanix', 'Gants avec protection des articulations', 6),
        (25, 'Milwaukee Cut Level 5', 160, 'Gris/Noir', 29.99, 'milwaukee_cut5_gris.jpg', 'Jardin & Équipement Pro', 'Milwaukee', 'Gants anti-coupure niveau 5 certifiés', 6);
'''
    mycursor.execute(sql)

    # Création de la table declinaison_gant
    sql='''
    CREATE TABLE declinaison_gant(
        id_declinaison_gant INT AUTO_INCREMENT,
        stock INT,
        prix_declinaison DECIMAL(19,2),
        image VARCHAR(50),
        taille_id INT NOT NULL,
        gant_id INT NOT NULL,
        PRIMARY KEY(id_declinaison_gant),
        FOREIGN KEY(taille_id) REFERENCES taille(id_taille),
        FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des déclinaisons de gants
    sql='''
    INSERT INTO declinaison_gant VALUES
        -- Specialized BG Grail (ID gant: 1)
        (1, 45, 39.99, 'specialized_grail_noir.jpg', 5, 1),
        (2, 38, 39.99, 'specialized_grail_rouge.jpg', 7, 1),
        
        -- Giro DND Cycling (ID gant: 2)
        (3, 52, 29.99, 'giro_dnd_noir.jpg', 5, 2),
        (4, 30, 29.99, 'giro_dnd_vert.jpg', 7, 2),
        
        -- Specialized Prime-Series (ID gant: 3)
        (5, 25, 54.99, 'specialized_prime_bleu.jpg', 6, 3),
        
        -- Decathlon Triban RC500 (ID gant: 4)
        (6, 60, 19.99, 'triban_rc500_noir.jpg', 5, 4),
        
        -- Fox Ranger Gel (ID gant: 5)
        (7, 42, 34.99, 'fox_ranger_gris.jpg', 6, 5),
        
        -- Venum Elite Boxing (ID gant: 6)
        (8, 18, 119.99, 'venum_elite_noir.jpg', 7, 6),
        (9, 15, 119.99, 'venum_elite_rouge.jpg', 9, 6),
        
        -- Everlast PowerLock (ID gant: 7)
        (10, 22, 89.99, 'everlast_power_noir.jpg', 7, 7),
        
        -- Venum Impact MMA (ID gant: 8)
        (11, 35, 69.99, 'venum_impact_noir.jpg', 5, 8),
        
        -- Everlast Pro Style (ID gant: 9)
        (12, 40, 44.99, 'everlast_pro_rouge.jpg', 5, 9),
        
        -- Adidas Speed 50 (ID gant: 10)
        (13, 30, 79.99, 'adidas_speed_bleu.jpg', 7, 10),
        
        -- The North Face Etip (ID gant: 11)
        (14, 55, 49.99, 'tnf_etip_noir.jpg', 5, 11),
        (15, 42, 49.99, 'tnf_etip_bleu.jpg', 7, 11),
        
        -- Columbia Thermarator (ID gant: 12)
        (16, 65, 34.99, 'columbia_therm_noir.jpg', 5, 12),
        
        -- The North Face Montana (ID gant: 13)
        (17, 28, 69.99, 'tnf_montana_noir.jpg', 6, 13),
        
        -- Columbia Whirlibird (ID gant: 14)
        (18, 35, 44.99, 'columbia_whirl_violet.jpg', 5, 14),
        
        -- Quechua SH500 (ID gant: 15)
        (19, 85, 24.99, 'quechua_sh500_noir.jpg', 5, 15),
        
        -- Rostaing Jardin Expert (ID gant: 16)
        (20, 80, 14.99, 'rostaing_expert_vert.jpg', 5, 16),
        (21, 75, 14.99, 'rostaing_expert_noir.jpg', 7, 16),
        
        -- Mapa Jardin Pro (ID gant: 17)
        (22, 95, 12.99, 'mapa_jardin_vert.jpg', 6, 17),
        
        -- Rostaing Rosier Premium (ID gant: 18)
        (23, 48, 18.99, 'rostaing_rosier_rose.jpg', 5, 18),
        
        -- Mechanix Garden Utility (ID gant: 19)
        (24, 60, 24.99, 'mechanix_garden_vert.jpg', 5, 19),
        
        -- Rossignol Ski Premium (ID gant: 20)
        (25, 25, 79.99, 'rossignol_ski_noir.jpg', 6, 20),
        
        -- The North Face Apex (ID gant: 21)
        (26, 20, 89.99, 'tnf_apex_blanc.jpg', 6, 21),
        
        -- Rossignol Tempest IMPR (ID gant: 22)
        (27, 18, 99.99, 'rossignol_tempest_rouge.jpg', 7, 22),
        
        -- Mechanix Original (ID gant: 23)
        (28, 70, 24.99, 'mechanix_orig_noir.jpg', 5, 23),
        
        -- Mechanix M-Pact (ID gant: 24)
        (29, 55, 34.99, 'mechanix_mpact_rouge.jpg', 6, 24),
        
        -- Milwaukee Cut Level 5 (ID gant: 25)
        (30, 50, 29.99, 'milwaukee_cut5_gris.jpg', 6, 25);

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
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des lignes de commande
    sql = '''
    INSERT INTO ligne_commande VALUES
        -- Commande 1 - Sophie Martin (Expédiée) - Vélo
        (1, 1, 1, 39.99),
        (1, 3, 2, 29.99),
        -- Commande 2 - Thomas Dubois (Expédiée) - Jardinage
        (2, 20, 3, 14.99),
        (2, 22, 2, 12.99),
        -- Commande 3 - Sophie Martin (En attente) - Combat + Hiver
        (3, 8, 1, 119.99),
        (3, 14, 1, 49.99),
        -- Commande 4 - Thomas Dubois (En attente) - Ski
        (4, 26, 1, 89.99),
        (4, 27, 1, 99.99),
        -- Commande 5 - Sophie Martin (Expédiée) - Hiver + Jardinage
        (5, 16, 2, 34.99),
        (5, 23, 1, 18.99),
        -- Commande 6 - Thomas Dubois (En attente) - Protection + Vélo
        (6, 29, 2, 34.99),
        (6, 7, 1, 34.99),
        -- Commande 7 - Sophie Martin (Expédiée) - Combat
        (7, 11, 1, 69.99),
        (7, 12, 1, 44.99);
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
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des lignes de panier
    sql = '''
    INSERT INTO ligne_panier VALUES
        -- Panier Sophie Martin
        (2, 10, 1, '2025-01-25'),
        (2, 18, 1, '2025-01-26'),
        (2, 24, 2, '2025-01-26'),
        -- Panier Thomas Dubois
        (3, 2, 1, '2025-01-25'),
        (3, 13, 1, '2025-01-27'),
        (3, 28, 1, '2025-01-27');
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
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des notes
    sql='''
    INSERT INTO note VALUES
        (2, 1, 5),
        (2, 11, 4),
        (3, 16, 5),
        (3, 20, 4)
    '''
    mycursor.execute(sql)

    # Création de la table commentaire
    sql='''
    CREATE TABLE commentaire(
        utilisateur_id INT,
        gant_id INT,
        date_publication DATE,
        commentaire VARCHAR(50),
        valider BOOLEAN,
        PRIMARY KEY(utilisateur_id, gant_id, date_publication),
        FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des commentaires
    sql='''
    INSERT INTO commentaire VALUES
        (2, 1, '2025-01-11', 'Excellents gants, très confortables !', 1),
        (3, 16, '2025-01-13', 'Parfaits pour le jardinage', 1),
        (2, 11, '2025-01-16', 'Bien mais un peu chers', 1);

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
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des historiques
    sql='''
    INSERT INTO historique VALUES
        (2, 1, '2025-01-09'),
        (2, 11, '2025-01-14'),
        (2, 6, '2025-01-15'),
        (3, 16, '2025-01-11'),
        (3, 20, '2025-01-17'),
        (3, 21, '2025-01-17');
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
    ) DEFAULT CHARSET=utf8
    '''
    mycursor.execute(sql)

    # Insertion des listes d'envies
    sql='''
    INSERT INTO liste_envie VALUES
        (2, 22, '2025-01-20'),
        (2, 24, '2025-01-22'),
        (3, 3, '2025-01-19'),
        (3, 13, '2025-01-21');
    '''
    mycursor.execute(sql)

    get_db().commit()
    mycursor.close()
    return redirect('/')
