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
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_adresse),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
) DEFAULT CHARSET UTF8;

CREATE TABLE couleur(
   id_couleur INT AUTO_INCREMENT,
   libelle_couleur VARCHAR(50),
   PRIMARY KEY(id_couleur)
) DEFAULT CHARSET UTF8;

CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATETIME,
   id_etat INT NOT NULL,
   id_utilisateur INT NOT NULL,
   id_adresse INT NOT NULL,
   id_adresse_1 INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_adresse) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_adresse_1) REFERENCES adresse(id_adresse)
) DEFAULT CHARSET UTF8;

CREATE TABLE gant(
   id_gant INT AUTO_INCREMENT,
   nom_gant VARCHAR(50),
   poids INT,
   prix_gant DECIMAL(19,4),
   photo VARCHAR(50),
   founisseur VARCHAR(50),
   marque VARCHAR(50),
   description VARCHAR(255),
   id_type_gant INT NOT NULL,
   PRIMARY KEY(id_gant),
   FOREIGN KEY(id_type_gant) REFERENCES type_gant(id_type_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE declinaison_gant(
   id_declinaison_gant INT AUTO_INCREMENT,
   stock INT,
   prix_declinaison INT,
   image VARCHAR(50),
   id_taille INT NOT NULL,
   id_couleur INT NOT NULL,
   id_gant INT NOT NULL,
   PRIMARY KEY(id_declinaison_gant),
   FOREIGN KEY(id_taille) REFERENCES taille(id_taille),
   FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE ligne_commande(
   id_commande INT,
   id_declinaison_gant INT,
   quantite INT,
   prix DECIMAL(19,4),
   PRIMARY KEY(id_commande, id_declinaison_gant),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
   FOREIGN KEY(id_declinaison_gant) REFERENCES declinaison_gant(id_declinaison_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE ligne_panier(
   id_utilisateur INT,
   id_declinaison_gant INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_utilisateur, id_declinaison_gant),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_declinaison_gant) REFERENCES declinaison_gant(id_declinaison_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE note(
   id_utilisateur INT,
   id_gant INT,
   note INT,
   PRIMARY KEY(id_utilisateur, id_gant),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE commentaire(
   id_utilisateur INT,
   id_gant INT,
   date_publication DATE,
   commentaire VARCHAR(50),
   valider BOOLEAN,
   PRIMARY KEY(id_utilisateur, id_gant, date_publication),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE historique(
   id_utilisateur INT,
   id_gant INT,
   date_consultation DATE,
   PRIMARY KEY(id_utilisateur, id_gant, date_consultation),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant)
) DEFAULT CHARSET UTF8;

CREATE TABLE liste_envie(
   id_utilisateur INT,
   id_gant INT,
   date_update DATE,
   PRIMARY KEY(id_utilisateur, id_gant, date_update),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant)
) DEFAULT CHARSET UTF8;


-- ============================
-- INSERT UTILISATEURS
-- ============================
INSERT INTO utilisateur(login, email, nom_utilisateur, password, role) VALUES
('admin', 'admin@example.com', 'Administrateur', 'admin', 'admin'),
('client', 'client@example.com', 'Client Un', 'client', 'client'),
('client2', 'client2@example.com', 'Client Deux', 'client2', 'client');

-- ============================
-- INSERT ETATS
-- ============================
INSERT INTO etat(libelle_etat) VALUES
('En état'),
('Expédiée');

-- ============================
-- INSERT TAILLES
-- ============================
INSERT INTO taille(num_taille_fr, taille_us, tour_de_main) VALUES
('7', 'S', '17 cm'),
('8', 'M', '19 cm'),
('9', 'L', '21 cm'),
('10', 'XL', '23 cm');

-- ============================
-- INSERT COULEURS
-- ============================
INSERT INTO couleur(libelle_couleur) VALUES
('Noir'),
('Bleu'),
('Rouge'),
('Gris'),
('Vert'),
('Jaune');

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
INSERT INTO adresse(nom_adresse, rue, code_postal, ville, date_utilisation, id_utilisateur) VALUES
('Maison', '1 rue du Centre', '25000', 'Besançon', '2024-01-01', 2),
('Travail', '12 avenue Victor Hugo', '25000', 'Besançon', '2024-02-01', 2),
('Maison', '5 rue des Lilas', '25200', 'Montbéliard', '2024-03-01', 3);

-- ============================
-- INSERT GANTS (1 par photo)
-- ============================
INSERT INTO gant(nom_gant, poids, prix_gant, photo, founisseur, marque, description, id_type_gant) VALUES
('Adidas Speed Bleu', 300, 59.99, 'adidas_speed_bleu.jpg', 'Adidas', 'Adidas', 'Gants de boxe rapides et légers', 1),
('Everlast Powerlock', 320, 79.99, 'everlast_powerlock.jpg', 'Everlast', 'Everlast', 'Gants de boxe Powerlock', 1),
('Rossignol Noir', 200, 49.99, 'gant_type_impr_rossignol_noir.jpg', 'Rossignol', 'Rossignol', 'Gants imprimés Rossignol', 4),
('Mechanix Garden', 150, 19.99, 'mechanix_garden.jpg', 'Mechanix', 'Mechanix', 'Gants de jardinage résistants', 2),
('Milwaukee Cut5 Gris', 180, 24.99, 'milwaukee_cut5_gris.jpg', 'Milwaukee', 'Milwaukee', 'Gants anti‑coupure niveau 5', 5),
('Rostaing Expert', 160, 22.99, 'rostaing_expert.jpg', 'Rostaing', 'Rostaing', 'Gants de jardinage expert', 2),
('Specialized Prime', 120, 34.99, 'specialized_prime.jpg', 'Specialized', 'Specialized', 'Gants vélo Prime', 3),
('TNF Montana', 250, 69.99, 'tnf_montana.jpg', 'The North Face', 'TNF', 'Gants chauds Montana', 6),
('Venum Impact', 330, 89.99, 'venum_impact.jpg', 'Venum', 'Venum', 'Gants de boxe Impact', 1),
('Columbia Therma', 210, 54.99, 'columbia_therma.jpg', 'Columbia', 'Columbia', 'Gants thermiques Columbia', 6),
('Everlast Prostyle', 310, 69.99, 'everlast_prostyle.jpg', 'Everlast', 'Everlast', 'Gants Prostyle', 1),
('Giro DND', 140, 29.99, 'giro_dnd.jpg', 'Giro', 'Giro', 'Gants vélo DND', 3),
('Mechanix Mpact', 190, 27.99, 'mechanix_mpact.jpg', 'Mechanix', 'Mechanix', 'Gants de travail Mpact', 5),
('Quechua SH500 Noir', 230, 39.99, 'quechua_sh500_noir.jpg', 'Quechua', 'Quechua', 'Gants hiver SH500', 6),
('Rostaing Rosier', 150, 17.99, 'rostaing_rosier.jpg', 'Rostaing', 'Rostaing', 'Gants pour rosiers', 2),
('TNF Apex', 240, 74.99, 'tnf_apex.jpg', 'The North Face', 'TNF', 'Gants Apex', 6),
('Triban RC500 Noir', 130, 24.99, 'triban_rc500_noir.jpg', 'Triban', 'Triban', 'Gants vélo RC500', 3),
('Columbia Whirli', 220, 49.99, 'columbia_whirli.jpg', 'Columbia', 'Columbia', 'Gants Whirlibird', 6),
('Fox Ranger Gris', 150, 29.99, 'fox_ranger_gris.jpg', 'Fox', 'Fox', 'Gants vélo Ranger', 3),
('Mapa Jardin', 110, 9.99, 'mapa_jardin.jpg', 'Mapa', 'Mapa', 'Gants de jardinage classiques', 2),
('Mechanix Original', 180, 25.99, 'mechanix_original.jpg', 'Mechanix', 'Mechanix', 'Gants Original', 5),
('Rossignol Ski', 260, 79.99, 'rossignol_ski.jpg', 'Rossignol', 'Rossignol', 'Gants de ski Rossignol', 4),
('Specialized Grail', 125, 32.99, 'specialized_grail.jpg', 'Specialized', 'Specialized', 'Gants vélo Grail', 3),
('TNF Etip', 140, 44.99, 'tnf_etip.jpg', 'The North Face', 'TNF', 'Gants tactiles Etip', 6),
('Venum Elite', 350, 99.99, 'venum_elite.jpg', 'Venum', 'Venum', 'Gants Elite', 1);

-- ============================
-- INSERT DECLINAISONS (1 taille + 1 couleur par gant)
-- ============================
INSERT INTO declinaison_gant(stock, prix_declinaison, image, id_taille, id_couleur, id_gant) VALUES
(20, 0, NULL, 2, 1, 1),
(15, 0, NULL, 3, 2, 2),
(10, 0, NULL, 2, 1, 3),
(30, 0, NULL, 1, 4, 4),
(25, 0, NULL, 3, 4, 5),
(18, 0, NULL, 2, 1, 6),
(22, 0, NULL, 2, 2, 7),
(12, 0, NULL, 3, 1, 8),
(14, 0, NULL, 3, 2, 9),
(16, 0, NULL, 2, 4, 10),
(20, 0, NULL, 3, 1, 11),
(25, 0, NULL, 2, 2, 12),
(30, 0, NULL, 3, 4, 13),
(18, 0, NULL, 2, 1, 14),
(22, 0, NULL, 1, 5, 15),
(12, 0, NULL, 3, 1, 16),
(14, 0, NULL, 2, 1, 17),
(16, 0, NULL, 3, 4, 18),
(20, 0, NULL, 2, 4, 19),
(25, 0, NULL, 1, 5, 20),
(30, 0, NULL, 3, 1, 21),
(18, 0, NULL, 2, 1, 22),
(22, 0, NULL, 2, 2, 23),
(12, 0, NULL, 3, 1, 24),
(14, 0, NULL, 3, 2, 25);

-- ============================
-- INSERT COMMANDES
-- ============================
INSERT INTO commande(date_achat, id_etat, id_utilisateur, id_adresse, id_adresse_1) VALUES
('2024-04-01 10:00:00', 1, 2, 1, 1),
('2024-04-05 15:30:00', 2, 3, 3, 3);

-- ============================
-- INSERT LIGNES DE COMMANDE
-- ============================
INSERT INTO ligne_commande VALUES
(1, 1, 2, 59.99),
(1, 3, 1, 49.99),
(2, 5, 1, 24.99);

-- ============================
-- INSERT PANIER
-- ============================
INSERT INTO ligne_panier VALUES
(2, 4, 1, '2024-04-10'),
(3, 7, 2, '2024-04-11');

-- ============================
-- INSERT NOTES
-- ============================
INSERT INTO note VALUES
(2, 1, 5),
(2, 9, 4),
(3, 12, 5);

-- ============================
-- INSERT COMMENTAIRES
-- ============================
INSERT INTO commentaire VALUES
(2, 1, '2024-04-12', 'Très bons gants', TRUE),
(3, 5, '2024-04-13', 'Bonne protection', TRUE);

-- ============================
-- INSERT HISTORIQUE
-- ============================
INSERT INTO historique VALUES
(2, 1, '2024-04-01'),
(2, 3, '2024-04-02'),
(3, 12, '2024-04-03');

-- ============================
-- INSERT LISTE D ENVIE
-- ============================
INSERT INTO liste_envie VALUES
(2, 9, '2024-04-15'),
(3, 25, '2024-04-16');
