DROP TABLE IF EXISTS liste_envie;
DROP TABLE IF EXISTS historique;
DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS declinaison_gant;
DROP TABLE IF EXISTS gant;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS type_gant;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(50),
   email VARCHAR(50),
   nom_utilisateur VARCHAR(50),
   password VARCHAR(255),
   role VARCHAR(50),
   PRIMARY KEY(id_utilisateur)
) DEFAULT CHARSET UTF8;

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(50),
   PRIMARY KEY(id_etat)
) DEFAULT CHARSET UTF8;

CREATE TABLE taille(
   id_taille INT AUTO_INCREMENT,
   num_taille_fr VARCHAR(50),
   taille_us VARCHAR(50),
   tour_de_main VARCHAR(50),
   PRIMARY KEY(id_taille)
) DEFAULT CHARSET UTF8;

CREATE TABLE type_gant(
   id_type_gant INT AUTO_INCREMENT,
   nom_type_gant VARCHAR(255),
   PRIMARY KEY(id_type_gant)
) DEFAULT CHARSET UTF8;

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
) DEFAULT CHARSET UTF8;

CREATE TABLE couleur(
   id_couleur INT AUTO_INCREMENT,
   libelle_couleur VARCHAR(50),
   code_couleur VARCHAR(255),
   PRIMARY KEY(id_couleur)
) DEFAULT CHARSET UTF8;

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
) DEFAULT CHARSET UTF8;

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
) DEFAULT CHARSET UTF8;

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
) DEFAULT CHARSET UTF8;

CREATE TABLE ligne_commande(
   commande_id INT,
   declinaison_gant_id INT,
   quantite INT,
   prix DECIMAL(19,2),
   PRIMARY KEY(commande_id, declinaison_gant_id),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
   FOREIGN KEY(declinaison_gant_id) REFERENCES declinaison_gant(id_declinaison_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE ligne_panier(
   utilisateur_id INT,
   declinaison_gant_id INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(utilisateur_id, declinaison_gant_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(declinaison_gant_id) REFERENCES declinaison_gant(id_declinaison_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE note(
   utilisateur_id INT,
   gant_id INT,
   note NUMERIC(2,1),
   PRIMARY KEY(utilisateur_id, gant_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE commentaire(
    utilisateur_id INT,
    gant_id INT,
    date_publication DATETIME,
    commentaire VARCHAR(50),
    valider BOOLEAN,
   PRIMARY KEY(utilisateur_id, gant_id, date_publication),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE historique(
   utilisateur_id INT,
   gant_id INT,
   date_consultation DATE,
   PRIMARY KEY(utilisateur_id, gant_id, date_consultation),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE liste_envie(
   utilisateur_id INT,
   gant_id INT,
   date_update DATE,
   PRIMARY KEY(utilisateur_id, gant_id, date_update),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
) DEFAULT CHARSET UTF8;


-- ============================
-- INSERT UTILISATEURS (inchangé)
-- ============================
INSERT INTO utilisateur(login, email, nom_utilisateur, password, role) VALUES
('admin', 'admin@example.com', 'Administrateur', 'pbkdf2:sha256:1000000$qwwvIJXyTvBTH4R1$73dd8f46cc5953965c9befed035509d47bb89b18166d02c2ee6b0924fb18f923', 'admin'),
('client', 'client@example.com', 'Client Un', 'pbkdf2:sha256:1000000$9u2VVssEqRYwvrze$b3ef9670d06f24ed3dc11a92f1cca4c7b00dd5c301d13bbedec2d6f1f0bb6eb0', 'client'),
('client2', 'client2@example.com', 'Client Deux', 'pbkdf2:sha256:1000000$Eq13PRiR0mkFGUej$4df2d53f486dc29e78c65a6ea3cc7004c4343bc58cdb8c91c19d43a3f84399fe', 'client');

-- ============================
-- INSERT ETATS (inchangé)
-- ============================
INSERT INTO etat(libelle_etat) VALUES
('En état'),
('Expédiée');

-- ============================
-- INSERT TAILLES
-- id_taille=1 : Taille unique (gants sans choix de taille)
-- id_taille=2 : 7 / S
-- id_taille=3 : 8 / M
-- id_taille=4 : 9 / L
-- id_taille=5 : 10 / XL
-- ============================
INSERT INTO taille(num_taille_fr, taille_us, tour_de_main) VALUES
('Taille unique', 'One size', 'Ajustable'),
('7', 'S', '17 cm'),
('8', 'M', '19 cm'),
('9', 'L', '21 cm'),
('10', 'XL', '23 cm');

-- ============================
-- INSERT TYPES DE GANTS
-- ============================
INSERT INTO type_gant(nom_type_gant) VALUES
('Boxe'),
('Jardinage'),
('Cyclisme'),
('Ski'),
('Travail'),
('Randonnée');

-- ============================
-- INSERT ADRESSES
-- ============================
INSERT INTO adresse(nom_adresse, rue, code_postal, ville, date_utilisation, utilisateur_id) VALUES
('Maison',  '1 rue du Centre',        '25000', 'Besançon',    '2024-01-01', 2),
('Travail', '12 avenue Victor Hugo',  '25000', 'Besançon',    '2024-02-01', 2),
('Maison',  '5 rue des Lilas',        '25200', 'Montbéliard', '2024-03-01', 3),
('Parents', '8 rue de la République', '25300', 'Pontarlier',  '2024-03-15', 3),

('Maison', '10 rue de Rivoli', '75001', 'Paris', '2024-01-01', 2),
('Travail', '25 avenue des Champs-Élysées', '75008', 'Paris', '2024-01-05', 2),

('Maison', '1 rue du Centre', '25000', 'Besançon', '2024-02-01', 2),
('Travail', '12 avenue Victor Hugo', '25000', 'Besançon', '2024-02-10', 2),

('Maison', '5 rue de la République', '69001', 'Lyon', '2024-03-01', 3),
('Parents', '8 rue Part-Dieu', '69003', 'Lyon', '2024-03-10', 3);

-- ============================
-- INSERT COULEURS
-- id_couleur=1 : Couleur unique (gants sans choix de couleur)
-- id_couleur=2 : Noir
-- id_couleur=3 : Bleu
-- id_couleur=4 : Rouge
-- id_couleur=5 : Gris
-- id_couleur=6 : Vert
-- id_couleur=7 : Jaune
-- id_couleur=8 : Blanc
-- id_couleur=9 : Orange
-- ============================
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

-- ============================
-- INSERT COMMANDES
-- ============================
INSERT INTO commande(date_achat, etat_id, utilisateur_id, adresse_id_livre, adresse_id_fact) VALUES
('2024-04-01 10:00:00', 1, 2, 1, 2),  -- id 1 : client, livraison Maison, fact Travail
('2024-04-05 15:30:00', 2, 3, 3, 3),  -- id 2 : client2, expédiée
('2024-04-20 09:15:00', 1, 2, 1, 2),  -- id 3 : client, en attente
('2024-05-03 14:00:00', 2, 3, 4, 4),  -- id 4 : client2, expédiée

-- =====================
-- ÎLE-DE-FRANCE
-- =====================
('2024-04-01 10:00:00', 1, 1, 1, 2),
('2024-04-01 11:00:00', 2, 2, 2, 2),
('2024-04-02 09:30:00', 1, 3, 3, 3),
('2024-04-02 14:00:00', 2, 1, 4, 4),
('2024-04-03 10:15:00', 1, 2, 1, 2),
('2024-04-03 16:20:00', 2, 3, 2, 2),
('2024-04-04 12:00:00', 1, 1, 3, 3),
('2024-04-04 18:45:00', 2, 2, 4, 4),
('2024-04-05 09:10:00', 1, 3, 1, 2),
('2024-04-05 13:30:00', 2, 1, 2, 2),

-- =====================
-- MARSEILLE (13)
-- =====================
('2024-04-06 10:00:00', 2, 2, 5, 5),
('2024-04-06 15:00:00', 1, 3, 5, 5),
('2024-04-07 11:30:00', 2, 1, 5, 5),

-- =====================
-- NANTES (44)
-- =====================
('2024-04-07 14:00:00', 1, 2, 6, 6),
('2024-04-08 09:45:00', 2, 3, 6, 6),
('2024-04-08 16:10:00', 1, 1, 6, 6),

-- =====================
-- RENNES (35)
-- =====================
('2024-04-09 10:20:00', 2, 2, 7, 7),
('2024-04-09 15:40:00', 1, 3, 7, 7),
('2024-04-10 11:10:00', 2, 1, 7, 7),

-- =====================
-- LYON (69)
-- =====================
('2024-04-10 14:00:00', 1, 2, 8, 8),
('2024-04-11 09:00:00', 2, 3, 8, 8),
('2024-04-11 17:30:00', 1, 1, 8, 8),

-- =====================
-- MIX (répartition réaliste)
-- =====================
('2024-04-12 10:00:00', 2, 2, 1, 2),
('2024-04-12 12:00:00', 1, 3, 5, 5),
('2024-04-12 18:00:00', 2, 1, 6, 6);

-- ============================
-- INSERT GANTS (mêmes photos qu'avant)
-- ============================
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
('TNF Etip',            140, 44.99,  'tnf_etip.jpg',                     'The North Face', 'TNF',       'Gants tactiles Etip connectivité',        6);  -- id 25

-- ============================
-- INSERT DECLINAISONS
--
-- Rappel tailles : 1=Taille unique, 2=S(7), 3=M(8), 4=L(9), 5=XL(10)
-- Rappel couleurs: 1=Couleur unique, 2=Noir, 3=Bleu, 4=Rouge, 5=Gris, 6=Vert, 7=Jaune, 8=Blanc, 9=Orange
--
-- Gants de BOXE  → tailles S/M/L/XL, plusieurs couleurs
-- Gants de SKI   → tailles S/M/L/XL, plusieurs couleurs
-- Gants VÉLO     → tailles S/M/L, 2 couleurs
-- Gants RANDO    → tailles S/M/L/XL, 2 couleurs
-- Gants JARDINAGE/TRAVAIL → taille unique ou 2 tailles, 1-2 couleurs
-- ============================

INSERT INTO declinaison_gant(stock, prix_declinaison, image, taille_id, couleur_id, gant_id) VALUES
-- -------------------------------------------------------
-- Gant 1 : Adidas Speed Bleu (59.99€) — 4 tailles × Bleu + 4 tailles × Noir
-- Bleu = couleur premium : +3€ = 62.99€ base
-- Noir = standard : 59.99€ base
-- déclinaisons id 1 à 8
-- -------------------------------------------------------
(15, 62.99, NULL, 2, 3, 1),   -- id 1  : S / Bleu = 62.99 + 0 = 63€
(20, 62.99, NULL, 3, 3, 1),   -- id 2  : M / Bleu = 62.99 + 0 = 63€
(18, 64.99, NULL, 4, 3, 1),   -- id 3  : L / Bleu = 62.99 + 2 = 65€
(10, 67.99, NULL, 5, 3, 1),   -- id 4  : XL / Bleu = 62.99 + 5 = 68€
(12, 59.99, NULL, 2, 2, 1),   -- id 5  : S / Noir = 59.99 + 0 = 60€
(16, 59.99, NULL, 3, 2, 1),   -- id 6  : M / Noir = 59.99 + 0 = 60€
(14, 61.99, NULL, 4, 2, 1),   -- id 7  : L / Noir = 59.99 + 2 = 62€
(8,  64.99, NULL, 5, 2, 1),   -- id 8  : XL / Noir = 59.99 + 5 = 65€

-- -------------------------------------------------------
-- Gant 2 : Everlast Powerlock (79.99€) — 4 tailles × Noir + 4 tailles × Rouge
-- Rouge = premium : +3€ = 82.99€ base
-- Noir = standard : 79.99€ base
-- déclinaisons id 9 à 16
-- -------------------------------------------------------
(20, 79.99, NULL, 2, 2, 2),   -- id 9  : S / Noir = 79.99 + 0 = 80€
(25, 79.99, NULL, 3, 2, 2),   -- id 10 : M / Noir = 79.99 + 0 = 80€
(22, 81.99, NULL, 4, 2, 2),   -- id 11 : L / Noir = 79.99 + 2 = 82€
(12, 84.99, NULL, 5, 2, 2),   -- id 12 : XL / Noir = 79.99 + 5 = 85€
(18, 82.99, NULL, 2, 4, 2),   -- id 13 : S / Rouge = 82.99 + 0 = 83€
(20, 82.99, NULL, 3, 4, 2),   -- id 14 : M / Rouge = 82.99 + 0 = 83€
(15, 84.99, NULL, 4, 4, 2),   -- id 15 : L / Rouge = 82.99 + 2 = 85€
(8,  87.99, NULL, 5, 4, 2),   -- id 16 : XL / Rouge = 82.99 + 5 = 88€

-- -------------------------------------------------------
-- Gant 3 : Venum Impact (89.99€) — 3 tailles × Noir + 3 tailles × Bleu
-- Bleu = premium : +3€ = 92.99€ base
-- Noir = standard : 89.99€ base
-- déclinaisons id 17 à 22
-- -------------------------------------------------------
(14, 89.99, NULL, 2, 2, 3),   -- id 17 : S / Noir = 89.99 + 0 = 90€
(18, 89.99, NULL, 3, 2, 3),   -- id 18 : M / Noir = 89.99 + 0 = 90€
(16, 91.99, NULL, 4, 2, 3),   -- id 19 : L / Noir = 89.99 + 2 = 92€
(12, 92.99, NULL, 2, 3, 3),   -- id 20 : S / Bleu = 92.99 + 0 = 93€
(16, 92.99, NULL, 3, 3, 3),   -- id 21 : M / Bleu = 92.99 + 0 = 93€
(10, 94.99, NULL, 4, 3, 3),   -- id 22 : L / Bleu = 92.99 + 2 = 95€

-- -------------------------------------------------------
-- Gant 4 : Everlast Prostyle (69.99€) — 4 tailles × Noir + 4 tailles × Bleu
-- Bleu = premium : +3€ = 72.99€ base
-- Noir = standard : 69.99€ base
-- déclinaisons id 23 à 30
-- -------------------------------------------------------
(16, 69.99, NULL, 2, 2, 4),   -- id 23 : S / Noir = 69.99 + 0 = 70€
(20, 69.99, NULL, 3, 2, 4),   -- id 24 : M / Noir = 69.99 + 0 = 70€
(18, 71.99, NULL, 4, 2, 4),   -- id 25 : L / Noir = 69.99 + 2 = 72€
(10, 74.99, NULL, 5, 2, 4),   -- id 26 : XL / Noir = 69.99 + 5 = 75€
(14, 72.99, NULL, 2, 3, 4),   -- id 27 : S / Bleu = 72.99 + 0 = 73€
(18, 72.99, NULL, 3, 3, 4),   -- id 28 : M / Bleu = 72.99 + 0 = 73€
(15, 74.99, NULL, 4, 3, 4),   -- id 29 : L / Bleu = 72.99 + 2 = 75€
(8,  77.99, NULL, 5, 3, 4),   -- id 30 : XL / Bleu = 72.99 + 5 = 78€

-- -------------------------------------------------------
-- Gant 5 : Venum Elite (99.99€) — 4 tailles × Noir + 4 tailles × Rouge
-- Rouge = premium : +3€ = 102.99€ base
-- Noir = standard : 99.99€ base
-- déclinaisons id 31 à 38
-- -------------------------------------------------------
(10, 99.99, NULL, 2, 2, 5),   -- id 31 : S / Noir = 99.99 + 0 = 100€
(15, 99.99, NULL, 3, 2, 5),   -- id 32 : M / Noir = 99.99 + 0 = 100€
(12, 101.99, NULL, 4, 2, 5),   -- id 33 : L / Noir = 99.99 + 2 = 102€
(6,  104.99, NULL, 5, 2, 5),   -- id 34 : XL / Noir = 99.99 + 5 = 105€
(8,  102.99, NULL, 2, 4, 5),   -- id 35 : S / Rouge = 102.99 + 0 = 103€
(12, 102.99, NULL, 3, 4, 5),   -- id 36 : M / Rouge = 102.99 + 0 = 103€
(10, 104.99, NULL, 4, 4, 5),   -- id 37 : L / Rouge = 102.99 + 2 = 105€
(5,  107.99, NULL, 5, 4, 5),   -- id 38 : XL / Rouge = 102.99 + 5 = 108€

-- -------------------------------------------------------
-- Gant 6 : Mechanix Garden (19.99€) — Taille unique × Vert + Taille unique × Bleu
-- Vert = standard : 19.99€
-- Bleu = premium : +3€ = 22.99€
-- déclinaisons id 39 à 40
-- -------------------------------------------------------
(35, 19.99, NULL, 1, 6, 6),   -- id 39 : Taille unique / Vert = 20€
(30, 22.99, NULL, 1, 3, 6),   -- id 40 : Taille unique / Bleu = 23€

-- -------------------------------------------------------
-- Gant 7 : Rostaing Expert (22.99€) — Taille unique × Vert
-- déclinaison id 41
-- -------------------------------------------------------
(40, 22.99, NULL, 1, 6, 7),   -- id 41 : Taille unique / Vert = 23€

-- -------------------------------------------------------
-- Gant 8 : Rostaing Rosier (17.99€) — Taille unique × Couleur unique
-- déclinaison id 42
-- -------------------------------------------------------
(50, 17.99, NULL, 1, 1, 8),   -- id 42 : Taille unique / Couleur unique = 18€

-- -------------------------------------------------------
-- Gant 9 : Mapa Jardin (9.99€) — Taille unique × Vert + Taille unique × Jaune
-- Vert = standard : 9.99€
-- Jaune = spécial : +5€ = 14.99€
-- déclinaisons id 43 à 44
-- -------------------------------------------------------
(60, 9.99, NULL, 1, 6, 9),   -- id 43 : Taille unique / Vert = 10€
(55, 14.99, NULL, 1, 7, 9),   -- id 44 : Taille unique / Jaune = 15€

-- -------------------------------------------------------
-- Gant 10 : Specialized Prime (34.99€) — 3 tailles × Bleu + 3 tailles × Noir
-- Bleu = premium : +3€ = 37.99€ base
-- Noir = standard : 34.99€ base
-- déclinaisons id 45 à 50
-- -------------------------------------------------------
(18, 37.99, NULL, 2, 3, 10),  -- id 45 : S / Bleu = 37.99 + 0 = 38€
(22, 37.99, NULL, 3, 3, 10),  -- id 46 : M / Bleu = 37.99 + 0 = 38€
(15, 39.99, NULL, 4, 3, 10),  -- id 47 : L / Bleu = 37.99 + 2 = 40€
(16, 34.99, NULL, 2, 2, 10),  -- id 48 : S / Noir = 34.99 + 0 = 35€
(20, 34.99, NULL, 3, 2, 10),  -- id 49 : M / Noir = 34.99 + 0 = 35€
(12, 36.99, NULL, 4, 2, 10),  -- id 50 : L / Noir = 34.99 + 2 = 37€

-- -------------------------------------------------------
-- Gant 11 : Giro DND (29.99€) — 3 tailles × Noir + 3 tailles × Gris
-- Noir/Gris = standard : 29.99€ base
-- déclinaisons id 51 à 56
-- -------------------------------------------------------
(20, 29.99, NULL, 2, 2, 11),  -- id 51 : S / Noir = 29.99 + 0 = 30€
(24, 29.99, NULL, 3, 2, 11),  -- id 52 : M / Noir = 29.99 + 0 = 30€
(18, 31.99, NULL, 4, 2, 11),  -- id 53 : L / Noir = 29.99 + 2 = 32€
(15, 29.99, NULL, 2, 5, 11),  -- id 54 : S / Gris = 29.99 + 0 = 30€
(20, 29.99, NULL, 3, 5, 11),  -- id 55 : M / Gris = 29.99 + 0 = 30€
(14, 31.99, NULL, 4, 5, 11),  -- id 56 : L / Gris = 29.99 + 2 = 32€

-- -------------------------------------------------------
-- Gant 12 : Triban RC500 Noir (24.99€) — 3 tailles × Noir
-- déclinaisons id 57 à 59
-- -------------------------------------------------------
(25, 24.99, NULL, 2, 2, 12),  -- id 57 : S / Noir = 24.99 + 0 = 25€
(30, 24.99, NULL, 3, 2, 12),  -- id 58 : M / Noir = 24.99 + 0 = 25€
(22, 26.99, NULL, 4, 2, 12),  -- id 59 : L / Noir = 24.99 + 2 = 27€

-- -------------------------------------------------------
-- Gant 13 : Specialized Grail (32.99€) — 3 tailles × Noir + 3 tailles × Bleu
-- Bleu = premium : +3€ = 35.99€ base
-- Noir = standard : 32.99€ base
-- déclinaisons id 60 à 65
-- -------------------------------------------------------
(12, 32.99, NULL, 2, 2, 13),  -- id 60 : S / Noir = 32.99 + 0 = 33€
(16, 32.99, NULL, 3, 2, 13),  -- id 61 : M / Noir = 32.99 + 0 = 33€
(14, 34.99, NULL, 4, 2, 13),  -- id 62 : L / Noir = 32.99 + 2 = 35€
(10, 35.99, NULL, 2, 3, 13),  -- id 63 : S / Bleu = 35.99 + 0 = 36€
(14, 35.99, NULL, 3, 3, 13),  -- id 64 : M / Bleu = 35.99 + 0 = 36€
(12, 37.99, NULL, 4, 3, 13),  -- id 65 : L / Bleu = 35.99 + 2 = 38€

-- -------------------------------------------------------
-- Gant 14 : Fox Ranger Gris (29.99€) — 3 tailles × Gris + 3 tailles × Orange
-- Gris = standard : 29.99€ base
-- Orange = spécial : +5€ = 34.99€ base
-- déclinaisons id 66 à 71
-- -------------------------------------------------------
(18, 29.99, NULL, 2, 5, 14),  -- id 66 : S / Gris = 29.99 + 0 = 30€
(22, 29.99, NULL, 3, 5, 14),  -- id 67 : M / Gris = 29.99 + 0 = 30€
(16, 31.99, NULL, 4, 5, 14),  -- id 68 : L / Gris = 29.99 + 2 = 32€
(15, 34.99, NULL, 2, 9, 14),  -- id 69 : S / Orange = 34.99 + 0 = 35€
(18, 34.99, NULL, 3, 9, 14),  -- id 70 : M / Orange = 34.99 + 0 = 35€
(12, 36.99, NULL, 4, 9, 14),  -- id 71 : L / Orange = 34.99 + 2 = 37€

-- -------------------------------------------------------
-- Gant 15 : Rossignol Noir (49.99€) — 4 tailles × Noir + 4 tailles × Bleu
-- Bleu = premium : +3€ = 52.99€ base
-- Noir = standard : 49.99€ base
-- déclinaisons id 72 à 79
-- -------------------------------------------------------
(12, 49.99, NULL, 2, 2, 15),  -- id 72 : S / Noir = 49.99 + 0 = 50€
(16, 49.99, NULL, 3, 2, 15),  -- id 73 : M / Noir = 49.99 + 0 = 50€
(14, 51.99, NULL, 4, 2, 15),  -- id 74 : L / Noir = 49.99 + 2 = 52€
(8,  54.99, NULL, 5, 2, 15),  -- id 75 : XL / Noir = 49.99 + 5 = 55€
(10, 52.99, NULL, 2, 3, 15),  -- id 76 : S / Bleu = 52.99 + 0 = 53€
(14, 52.99, NULL, 3, 3, 15),  -- id 77 : M / Bleu = 52.99 + 0 = 53€
(12, 54.99, NULL, 4, 3, 15),  -- id 78 : L / Bleu = 52.99 + 2 = 55€
(6,  57.99, NULL, 5, 3, 15),  -- id 79 : XL / Bleu = 52.99 + 5 = 58€

-- -------------------------------------------------------
-- Gant 16 : Rossignol Ski (79.99€) — 4 tailles × Noir + 4 tailles × Rouge
-- Rouge = premium : +3€ = 82.99€ base
-- Noir = standard : 79.99€ base
-- déclinaisons id 80 à 87
-- -------------------------------------------------------
(10, 79.99, NULL, 2, 2, 16),  -- id 80 : S / Noir = 79.99 + 0 = 80€
(14, 79.99, NULL, 3, 2, 16),  -- id 81 : M / Noir = 79.99 + 0 = 80€
(12, 81.99, NULL, 4, 2, 16),  -- id 82 : L / Noir = 79.99 + 2 = 82€
(6,  84.99, NULL, 5, 2, 16),  -- id 83 : XL / Noir = 79.99 + 5 = 85€
(8,  82.99, NULL, 2, 4, 16),  -- id 84 : S / Rouge = 82.99 + 0 = 83€
(12, 82.99, NULL, 3, 4, 16),  -- id 85 : M / Rouge = 82.99 + 0 = 83€
(10, 84.99, NULL, 4, 4, 16),  -- id 86 : L / Rouge = 82.99 + 2 = 85€
(5,  87.99, NULL, 5, 4, 16),  -- id 87 : XL / Rouge = 82.99 + 5 = 88€

-- -------------------------------------------------------
-- Gant 17 : Milwaukee Cut5 Gris (24.99€) — 4 tailles × Gris + 4 tailles × Orange
-- Gris = standard : 24.99€ base
-- Orange = spécial : +5€ = 29.99€ base
-- déclinaisons id 88 à 95
-- -------------------------------------------------------
(20, 24.99, NULL, 2, 5, 17),  -- id 88 : S / Gris = 24.99 + 0 = 25€
(25, 24.99, NULL, 3, 5, 17),  -- id 89 : M / Gris = 24.99 + 0 = 25€
(22, 26.99, NULL, 4, 5, 17),  -- id 90 : L / Gris = 24.99 + 2 = 27€
(15, 29.99, NULL, 5, 5, 17),  -- id 91 : XL / Gris = 24.99 + 5 = 30€
(18, 29.99, NULL, 2, 9, 17),  -- id 92 : S / Orange = 29.99 + 0 = 30€
(22, 29.99, NULL, 3, 9, 17),  -- id 93 : M / Orange = 29.99 + 0 = 30€
(20, 31.99, NULL, 4, 9, 17),  -- id 94 : L / Orange = 29.99 + 2 = 32€
(12, 34.99, NULL, 5, 9, 17),  -- id 95 : XL / Orange = 29.99 + 5 = 35€

-- -------------------------------------------------------
-- Gant 18 : Mechanix Mpact (27.99€) — 4 tailles × Noir + 4 tailles × Gris
-- Noir/Gris = standard : 27.99€ base
-- déclinaisons id 96 à 103
-- -------------------------------------------------------
(18, 27.99, NULL, 2, 2, 18),  -- id 96  : S / Noir = 27.99 + 0 = 28€
(22, 27.99, NULL, 3, 2, 18),  -- id 97  : M / Noir = 27.99 + 0 = 28€
(20, 29.99, NULL, 4, 2, 18),  -- id 98  : L / Noir = 27.99 + 2 = 30€
(14, 32.99, NULL, 5, 2, 18),  -- id 99  : XL / Noir = 27.99 + 5 = 33€
(16, 27.99, NULL, 2, 5, 18),  -- id 100 : S / Gris = 27.99 + 0 = 28€
(20, 27.99, NULL, 3, 5, 18),  -- id 101 : M / Gris = 27.99 + 0 = 28€
(18, 29.99, NULL, 4, 5, 18),  -- id 102 : L / Gris = 27.99 + 2 = 30€
(10, 32.99, NULL, 5, 5, 18),  -- id 103 : XL / Gris = 27.99 + 5 = 33€

-- -------------------------------------------------------
-- Gant 19 : Mechanix Original (25.99€) — 4 tailles × Noir
-- déclinaisons id 104 à 107
-- -------------------------------------------------------
(25, 25.99, NULL, 2, 2, 19),  -- id 104 : S / Noir = 25.99 + 0 = 26€
(30, 25.99, NULL, 3, 2, 19),  -- id 105 : M / Noir = 25.99 + 0 = 26€
(28, 27.99, NULL, 4, 2, 19),  -- id 106 : L / Noir = 25.99 + 2 = 28€
(18, 30.99, NULL, 5, 2, 19),  -- id 107 : XL / Noir = 25.99 + 5 = 31€

-- -------------------------------------------------------
-- Gant 20 : TNF Montana (69.99€) — 4 tailles × Noir + 4 tailles × Bleu
-- Bleu = premium : +3€ = 72.99€ base
-- Noir = standard : 69.99€ base
-- déclinaisons id 108 à 115
-- -------------------------------------------------------
(12, 69.99, NULL, 2, 2, 20),  -- id 108 : S / Noir = 69.99 + 0 = 70€
(16, 69.99, NULL, 3, 2, 20),  -- id 109 : M / Noir = 69.99 + 0 = 70€
(14, 71.99, NULL, 4, 2, 20),  -- id 110 : L / Noir = 69.99 + 2 = 72€
(8,  74.99, NULL, 5, 2, 20),  -- id 111 : XL / Noir = 69.99 + 5 = 75€
(10, 72.99, NULL, 2, 3, 20),  -- id 112 : S / Bleu = 72.99 + 0 = 73€
(14, 72.99, NULL, 3, 3, 20),  -- id 113 : M / Bleu = 72.99 + 0 = 73€
(12, 74.99, NULL, 4, 3, 20),  -- id 114 : L / Bleu = 72.99 + 2 = 75€
(6,  77.99, NULL, 5, 3, 20),  -- id 115 : XL / Bleu = 72.99 + 5 = 78€

-- -------------------------------------------------------
-- Gant 21 : Columbia Therma (54.99€) — 4 tailles × Noir + 4 tailles × Rouge
-- Rouge = premium : +3€ = 57.99€ base
-- Noir = standard : 54.99€ base
-- déclinaisons id 116 à 123
-- -------------------------------------------------------
(14, 54.99, NULL, 2, 2, 21),  -- id 116 : S / Noir = 54.99 + 0 = 55€
(18, 54.99, NULL, 3, 2, 21),  -- id 117 : M / Noir = 54.99 + 0 = 55€
(16, 56.99, NULL, 4, 2, 21),  -- id 118 : L / Noir = 54.99 + 2 = 57€
(10, 59.99, NULL, 5, 2, 21),  -- id 119 : XL / Noir = 54.99 + 5 = 60€
(12, 57.99, NULL, 2, 4, 21),  -- id 120 : S / Rouge = 57.99 + 0 = 58€
(16, 57.99, NULL, 3, 4, 21),  -- id 121 : M / Rouge = 57.99 + 0 = 58€
(14, 59.99, NULL, 4, 4, 21),  -- id 122 : L / Rouge = 57.99 + 2 = 60€
(8,  62.99, NULL, 5, 4, 21),  -- id 123 : XL / Rouge = 57.99 + 5 = 63€

-- -------------------------------------------------------
-- Gant 22 : TNF Apex (74.99€) — 4 tailles × Noir + 4 tailles × Gris
-- Noir/Gris = standard : 74.99€ base
-- déclinaisons id 124 à 131
-- -------------------------------------------------------
(10, 74.99, NULL, 2, 2, 22),  -- id 124 : S / Noir = 74.99 + 0 = 75€
(14, 74.99, NULL, 3, 2, 22),  -- id 125 : M / Noir = 74.99 + 0 = 75€
(12, 76.99, NULL, 4, 2, 22),  -- id 126 : L / Noir = 74.99 + 2 = 77€
(6,  79.99, NULL, 5, 2, 22),  -- id 127 : XL / Noir = 74.99 + 5 = 80€
(8,  74.99, NULL, 2, 5, 22),  -- id 128 : S / Gris = 74.99 + 0 = 75€
(12, 74.99, NULL, 3, 5, 22),  -- id 129 : M / Gris = 74.99 + 0 = 75€
(10, 76.99, NULL, 4, 5, 22),  -- id 130 : L / Gris = 74.99 + 2 = 77€
(5,  79.99, NULL, 5, 5, 22),  -- id 131 : XL / Gris = 74.99 + 5 = 80€

-- -------------------------------------------------------
-- Gant 23 : Quechua SH500 Noir (39.99€) — 4 tailles × Noir
-- déclinaisons id 132 à 135
-- -------------------------------------------------------
(20, 39.99, NULL, 2, 2, 23),  -- id 132 : S / Noir = 39.99 + 0 = 40€
(25, 39.99, NULL, 3, 2, 23),  -- id 133 : M / Noir = 39.99 + 0 = 40€
(22, 41.99, NULL, 4, 2, 23),  -- id 134 : L / Noir = 39.99 + 2 = 42€
(15, 44.99, NULL, 5, 2, 23),  -- id 135 : XL / Noir = 39.99 + 5 = 45€

-- -------------------------------------------------------
-- Gant 24 : Columbia Whirli (49.99€) — 4 tailles × Noir + 4 tailles × Bleu
-- Bleu = premium : +3€ = 52.99€ base
-- Noir = standard : 49.99€ base
-- déclinaisons id 136 à 143
-- -------------------------------------------------------
(12, 49.99, NULL, 2, 2, 24),  -- id 136 : S / Noir = 49.99 + 0 = 50€
(16, 49.99, NULL, 3, 2, 24),  -- id 137 : M / Noir = 49.99 + 0 = 50€
(14, 51.99, NULL, 4, 2, 24),  -- id 138 : L / Noir = 49.99 + 2 = 52€
(8,  54.99, NULL, 5, 2, 24),  -- id 139 : XL / Noir = 49.99 + 5 = 55€
(10, 52.99, NULL, 2, 3, 24),  -- id 140 : S / Bleu = 52.99 + 0 = 53€
(14, 52.99, NULL, 3, 3, 24),  -- id 141 : M / Bleu = 52.99 + 0 = 53€
(12, 54.99, NULL, 4, 3, 24),  -- id 142 : L / Bleu = 52.99 + 2 = 55€
(6,  57.99, NULL, 5, 3, 24),  -- id 143 : XL / Bleu = 52.99 + 5 = 58€

-- -------------------------------------------------------
-- Gant 25 : TNF Etip (44.99€) — 4 tailles × Noir + 4 tailles × Gris
-- Noir/Gris = standard : 44.99€ base
-- déclinaisons id 144 à 151
-- -------------------------------------------------------
(14, 44.99, NULL, 2, 2, 25),  -- id 144 : S / Noir = 44.99 + 0 = 45€
(18, 44.99, NULL, 3, 2, 25),  -- id 145 : M / Noir = 44.99 + 0 = 45€
(16, 46.99, NULL, 4, 2, 25),  -- id 146 : L / Noir = 44.99 + 2 = 47€
(10, 49.99, NULL, 5, 2, 25),  -- id 147 : XL / Noir = 44.99 + 5 = 50€
(12, 44.99, NULL, 2, 5, 25),  -- id 148 : S / Gris = 44.99 + 0 = 45€
(16, 44.99, NULL, 3, 5, 25),  -- id 149 : M / Gris = 44.99 + 0 = 45€
(14, 46.99, NULL, 4, 5, 25),  -- id 150 : L / Gris = 44.99 + 2 = 47€
(8,  49.99, NULL, 5, 5, 25);  -- id 151 : XL / Gris = 44.99 + 5 = 50€


-- ============================
-- INSERT LIGNES DE COMMANDE
-- Références aux déclinaisons :
--   id 2  = Adidas Speed Bleu M/Bleu       (gant 1)
--   id 24 = Everlast Prostyle M/Noir        (gant 4)
--   id 89 = Milwaukee Cut5 M/Gris           (gant 17)
--   id 58 = Triban RC500 M/Noir             (gant 12)
--   id 117= Columbia Therma M/Noir          (gant 21)
--   id 33 = Venum Elite L/Noir              (gant 5)
--   id 113= TNF Montana M/Bleu              (gant 20)
-- ============================
INSERT INTO ligne_commande VALUES
(1, 2,  2, 59.99),   -- commande 1 : Adidas Speed Bleu M/Bleu, qté 2
(1, 24, 1, 69.99),   -- commande 1 : Everlast Prostyle M/Noir, qté 1
(2, 89, 2, 24.99),   -- commande 2 : Milwaukee Cut5 M/Gris, qté 2
(2, 58, 1, 24.99),   -- commande 2 : Triban RC500 M/Noir, qté 1
(3, 117,1, 54.99),   -- commande 3 : Columbia Therma M/Noir, qté 1
(3, 33, 1, 99.99),   -- commande 3 : Venum Elite L/Noir, qté 1
(4, 113,2, 69.99),   -- commande 4 : TNF Montana M/Bleu, qté 2
(4, 89, 3, 24.99),  -- commande 4 : Milwaukee Cut5 M/Gris, qté 3


-- =====================
-- MARSEILLE (11 à 13) gros CA
-- =====================
(11, 33, 3, 99.99),
(12, 113,2, 69.99),
(13, 33, 1, 99.99),

-- =====================
-- NANTES (14 à 16)
-- =====================
(14, 58, 2, 24.99),
(15, 117,1, 54.99),
(16, 89, 2, 24.99),

-- =====================
-- RENNES (17 à 19)
-- =====================
(17, 2, 2, 59.99),
(18, 24, 1, 69.99),
(19, 33, 1, 99.99),

-- =====================
-- LYON (20 à 22)
-- =====================
(20, 117,1, 54.99),
(21, 24, 2, 69.99),
(22, 2, 1, 59.99),

-- =====================
-- MIX (23 à 25)
-- =====================
(23, 89, 2, 24.99),
(24, 113,1, 69.99),
(25, 33, 1, 99.99);

-- ============================
-- INSERT PANIER
-- Références aux déclinaisons :
--   id 36  = Venum Elite M/Rouge  (gant 5)
--   id 46  = Specialized Prime M/Bleu (gant 10)
--   id 125 = TNF Apex M/Noir (gant 22)
--   id 67  = Fox Ranger M/Gris (gant 14)
-- ============================
INSERT INTO ligne_panier VALUES
(2, 36,  1, '2024-04-10'),  -- client : Venum Elite M/Rouge
(2, 125, 1, '2024-04-11'),  -- client : TNF Apex M/Noir
(3, 46,  2, '2024-04-12'),  -- client2 : Specialized Prime M/Bleu
(3, 67,  1, '2024-04-14'),  -- client2 : Fox Ranger M/Gris

(1, 36, 1, '2024-04-10'),
(1, 125,1, '2024-04-11'),
(2, 46, 2, '2024-04-12'),
(2, 67, 1, '2024-04-13'),
(3, 58, 1, '2024-04-14'),
(3, 89, 2, '2024-04-15');

-- ============================
-- INSERT NOTES
-- ============================
INSERT INTO note VALUES
(2, 1,  5.0),   -- client note Adidas Speed Bleu : 5/5
(2, 4,  4.5),   -- client note Everlast Prostyle : 4/5
(2, 10, 5.0),   -- client note Specialized Prime : 5/5
(3, 12, 4.0),   -- client2 note Triban RC500 : 4/5
(3, 17, 5.0),   -- client2 note Milwaukee Cut5 : 5/5
(3, 21, 3.0);   -- client2 note Columbia Therma : 3/5

-- ============================
-- INSERT COMMENTAIRES
-- ============================
INSERT INTO commentaire VALUES
(2, 1,  '2024-04-12 10:00:00', 'Très bons gants de boxe',  TRUE),
(2, 4,  '2024-04-15 11:00:00', 'Bon rapport qualité prix', TRUE),
(2, 10, '2024-04-18 12:00:00', 'Parfaits pour le vélo',    TRUE),
(3, 12, '2024-04-20 09:00:00', 'Légers et confortables',   TRUE),
(3, 17, '2024-04-22 14:00:00', 'Très bonne protection',    FALSE),
(3, 21, '2024-04-25 16:00:00', 'Corrects mais un peu fins', TRUE);

-- ============================
-- INSERT HISTORIQUE
-- ============================
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
(3, 25, '2024-04-07');

-- ============================
-- INSERT LISTE D'ENVIE
-- ============================
INSERT INTO liste_envie VALUES
(2, 5,  '2024-04-15'),  -- client veut Venum Elite
(2, 22, '2024-04-16'),  -- client veut TNF Apex
(2, 16, '2024-04-17'),  -- client veut Rossignol Ski
(3, 1,  '2024-04-15'),  -- client2 veut Adidas Speed Bleu
(3, 25, '2024-04-16'),  -- client2 veut TNF Etip
(3, 10, '2024-04-18');  -- client2 veut Specialized Prime