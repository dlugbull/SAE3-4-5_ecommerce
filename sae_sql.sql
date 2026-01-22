DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS est_de_taille;
DROP TABLE IF EXISTS est_de_couleur;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS gant;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS fournisseur;
DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS type;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS etat;


CREATE TABLE etat(
    id_etat INT,
    libelle_etat VARCHAR(50),
    PRIMARY KEY(id_etat)
);

CREATE TABLE taille(
    id_taille INT,
    taille_france VARCHAR(50),
    taille_us VARCHAR(50),
    tour_main VARCHAR(50),
    PRIMARY KEY(id_taille)
);

CREATE TABLE couleur(
    id_couleur INT,
    libelle_couleur VARCHAR(50),
    PRIMARY KEY(id_couleur)
);

CREATE TABLE type(
    id_type INT,
    nom_type VARCHAR(50),
    PRIMARY KEY(id_type)
);

CREATE TABLE marque(
    id_marque INT,
    nom_marque VARCHAR(50),
    PRIMARY KEY(id_marque)
);

CREATE TABLE fournisseur(
    id_fournisseur VARCHAR(50),
    nom_fournisseur VARCHAR(50),
    PRIMARY KEY(id_fournisseur)
);

CREATE TABLE role(
    id_role INT,
    nom_role VARCHAR(50),
    PRIMARY KEY(id_role)
);

CREATE TABLE utilisateur(
    id_utilisateur VARCHAR(50),
    login VARCHAR(50),
    email VARCHAR(50),
    nom_utilisateur VARCHAR(50),
    password VARCHAR(255),
    role_id INT NOT NULL,
    PRIMARY KEY(id_utilisateur),
    CONSTRAINT fk_utilisateur_role
        FOREIGN KEY(role_id) REFERENCES role(id_role)
);

CREATE TABLE commande(
    id_commande INT,
    date_commande DATETIME,
    etat_id INT NOT NULL,
    utilisateur_id VARCHAR(50) NOT NULL,
    PRIMARY KEY(id_commande),
    CONSTRAINT fk_commande_etat
        FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
    CONSTRAINT fk_commande_utilisateur
        FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE gant(
    id_gant INT,
    nom_gant VARCHAR(50),
    poids INT,
    prix_gant DECIMAL(19,4),
    photo VARCHAR(50),
    marque_id INT NOT NULL,
    fournisseur_id VARCHAR(50) NOT NULL,
    type_id INT NOT NULL,
    PRIMARY KEY(id_gant),
    CONSTRAINT fk_gant_marque
        FOREIGN KEY(marque_id) REFERENCES marque(id_marque),
    CONSTRAINT fk_gant_fournisseur
        FOREIGN KEY(fournisseur_id) REFERENCES fournisseur(id_fournisseur),
    CONSTRAINT fk_gant_type
        FOREIGN KEY(type_id) REFERENCES type(id_type)
);

CREATE TABLE ligne_commande(
    commande_id INT,
    gant_id INT,
    quantite INT,
    prix DECIMAL(19,4),
    PRIMARY KEY(commande_id, gant_id),
    CONSTRAINT fk_ligne_commande_commande
        FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
    CONSTRAINT fk_ligne_commande_gant
        FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
);

CREATE TABLE est_de_couleur(
    gant_id INT,
    couleur_id INT,
    PRIMARY KEY(gant_id, couleur_id),
    CONSTRAINT fk_est_de_couleur_gant
        FOREIGN KEY(gant_id) REFERENCES gant(id_gant),
    CONSTRAINT fk_est_de_couleur_couleur
        FOREIGN KEY(couleur_id) REFERENCES couleur(id_couleur)
);

CREATE TABLE est_de_taille(
    gant_id INT,
    taille_id INT,
    stock INT,
    PRIMARY KEY(gant_id, taille_id),
    CONSTRAINT fk_est_de_taille_gant
        FOREIGN KEY(gant_id) REFERENCES gant(id_gant),
    CONSTRAINT fk_est_de_taille_taille
        FOREIGN KEY(taille_id) REFERENCES taille(id_taille)
);

CREATE TABLE ligne_panier(
    utilisateur_id VARCHAR(50),
    gant_id INT,
    quantite INT,
    date_ajout DATE,
    PRIMARY KEY(utilisateur_id, gant_id),
    CONSTRAINT fk_ligne_panier_utilisateur
        FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    CONSTRAINT fk_ligne_panier_gant
        FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
);

-- ============================================
-- JEU DE DONNÉES DE TEST - SYSTÈME DE GANTS
-- ============================================

-- ÉTATS DE COMMANDE
INSERT INTO etat VALUES
(1, 'En attente'),
(2, 'Expédiée');

-- TAILLES
INSERT INTO taille VALUES
(1, '6', 'XS', '15-16 cm'),
(2, '8', 'S', '17-18 cm'),
(3, '10', 'M', '19-20 cm'),
(4, '12', 'L', '21-22 cm'),
(5, '14', 'XL', '23-24 cm'),
(6, '16', 'XXL', '25-26 cm');

-- COULEURS
INSERT INTO couleur VALUES
(1, 'Noir'),
(2, 'Rouge'),
(3, 'Bleu'),
(4, 'Blanc'),
(5, 'Or'),
(6, 'Argent'),
(7, 'Rose'),
(8, 'Vert'),
(9, 'Violet'),
(10, 'Orange');

-- TYPES D'ARTICLES
INSERT INTO type VALUES
(1, 'Gants de Vélo'),
(2, 'Gants de Sport Combat'),
(3, 'Gants d''Hiver'),
(4, 'Gants de Jardinage'),
(5, 'Gants de Ski'),
(6, 'Gants de Protection');

-- MARQUES
INSERT INTO marque VALUES
(1, 'Specialized'),
(2, 'Venum'),
(3, 'The North Face'),
(4, 'Rostaing'),
(5, 'Rossignol'),
(6, 'Mechanix Wear'),
(7, 'Giro'),
(8, 'Columbia'),
(9, 'Everlast'),
(10, 'Mapa');

-- FOURNISSEURS
INSERT INTO fournisseur VALUES
('F001', 'Sport 2000 Distribution'),
('F002', 'Jardin & Équipement Pro'),
('F003', 'Outdoor Adventure Supply'),
('F004', 'Combat Sports France'),
('F005', 'Mountain Gear Europe');

-- RÔLES
INSERT INTO role VALUES
(1, 'Client'),
(2, 'Administrateur'),
(3, 'Gérant'),
(4, 'Vendeur');

-- UTILISATEURS
INSERT INTO utilisateur VALUES
('U001', 'jean.dupont', 'jean.dupont@email.com', 'Jean Dupont', '$2y$10$hashed_password_1', 1),
('U002', 'marie.martin', 'marie.martin@email.com', 'Marie Martin', '$2y$10$hashed_password_2', 1),
('U003', 'admin', 'admin@boutique-gants.fr', 'Administrateur', '$2y$10$hashed_password_3', 2),
('U004', 'paul.bernard', 'paul.bernard@email.com', 'Paul Bernard', '$2y$10$hashed_password_4', 1),
('U005', 'sophie.petit', 'sophie.petit@email.com', 'Sophie Petit', '$2y$10$hashed_password_5', 1),
('U006', 'vendeur1', 'vendeur@boutique-gants.fr', 'Lucas Vendeur', '$2y$10$hashed_password_6', 4);

-- GANTS (20 articles variés)
INSERT INTO gant VALUES
-- Gants de Vélo
(1, 'Specialized BG Grail', 85, 39.99, 'specialized_grail.jpg', 1, 'F001', 1),
(2, 'Giro DND Cycling', 75, 29.99, 'giro_dnd.jpg', 7, 'F001', 1),
(3, 'Specialized Prime-Series', 95, 54.99, 'specialized_prime.jpg', 1, 'F001', 1),

-- Gants de Sport Combat
(4, 'Venum Elite Boxing', 420, 119.99, 'venum_elite.jpg', 2, 'F004', 2),
(5, 'Everlast PowerLock', 450, 89.99, 'everlast_powerlock.jpg', 9, 'F004', 2),
(6, 'Venum Impact MMA', 280, 69.99, 'venum_impact.jpg', 2, 'F004', 2),
(7, 'Everlast Pro Style', 380, 44.99, 'everlast_prostyle.jpg', 9, 'F004', 2),

-- Gants d'Hiver
(8, 'The North Face Etip', 120, 49.99, 'tnf_etip.jpg', 3, 'F003', 3),
(9, 'Columbia Thermarator', 140, 34.99, 'columbia_therma.jpg', 8, 'F003', 3),
(10, 'The North Face Montana', 180, 69.99, 'tnf_montana.jpg', 3, 'F003', 3),
(11, 'Columbia Whirlibird', 160, 44.99, 'columbia_whirli.jpg', 8, 'F003', 3),

-- Gants de Jardinage
(12, 'Rostaing Jardin Expert', 95, 14.99, 'rostaing_expert.jpg', 4, 'F002', 4),
(13, 'Mapa Jardin Pro', 110, 12.99, 'mapa_jardin.jpg', 10, 'F002', 4),
(14, 'Rostaing Rosier Premium', 85, 18.99, 'rostaing_rosier.jpg', 4, 'F002', 4),
(15, 'Mechanix Garden Utility', 100, 24.99, 'mechanix_garden.jpg', 6, 'F002', 4),

-- Gants de Ski
(16, 'Rossignol Ski Premium', 220, 79.99, 'rossignol_ski.jpg', 5, 'F005', 5),
(17, 'The North Face Apex', 200, 89.99, 'tnf_apex.jpg', 3, 'F005', 5),
(18, 'Rossignol Tempest IMPR', 240, 99.99, 'rossignol_tempest.jpg', 5, 'F005', 5),

-- Gants de Protection
(19, 'Mechanix Original', 130, 24.99, 'mechanix_original.jpg', 6, 'F001', 6),
(20, 'Mechanix M-Pact', 150, 34.99, 'mechanix_mpact.jpg', 6, 'F001', 6);

-- ASSOCIATION GANTS-COULEURS
INSERT INTO est_de_couleur VALUES
-- Specialized BG Grail (Vélo)
(1, 1), (1, 2), (1, 3),
-- Giro DND (Vélo)
(2, 1), (2, 8), (2, 10),
-- Specialized Prime (Vélo)
(3, 1), (3, 2), (3, 4),
-- Venum Elite (Combat)
(4, 1), (4, 2), (4, 4),
-- Everlast PowerLock (Combat)
(5, 1), (5, 2), (5, 3),
-- Venum Impact MMA (Combat)
(6, 1), (6, 2),
-- Everlast Pro Style (Combat)
(7, 1), (7, 2), (7, 3), (7, 7),
-- The North Face Etip (Hiver)
(8, 1), (8, 3), (8, 6),
-- Columbia Thermarator (Hiver)
(9, 1), (9, 3), (9, 2),
-- The North Face Montana (Hiver)
(10, 1), (10, 3), (10, 8),
-- Columbia Whirlibird (Hiver)
(11, 1), (11, 2), (11, 9),
-- Rostaing Jardin Expert (Jardinage)
(12, 8), (12, 1), (12, 3),
-- Mapa Jardin Pro (Jardinage)
(13, 8), (13, 10),
-- Rostaing Rosier (Jardinage)
(14, 1), (14, 8), (14, 7),
-- Mechanix Garden (Jardinage)
(15, 8), (15, 1),
-- Rossignol Ski (Ski)
(16, 1), (16, 2), (16, 3),
-- The North Face Apex (Ski)
(17, 1), (17, 4), (17, 5),
-- Rossignol Tempest (Ski)
(18, 1), (18, 2), (18, 10),
-- Mechanix Original (Protection)
(19, 1), (19, 2), (19, 10),
-- Mechanix M-Pact (Protection)
(20, 1), (20, 3), (20, 2);

-- STOCK PAR TAILLE (distribution réaliste des stocks)
INSERT INTO est_de_taille VALUES
-- Specialized BG Grail (Vélo - XS à XL)
(1, 1, 8), (1, 2, 20), (1, 3, 25), (1, 4, 22), (1, 5, 12),
-- Giro DND (Vélo - S à XL)
(2, 2, 25), (2, 3, 35), (2, 4, 30), (2, 5, 15),
-- Specialized Prime (Vélo - XS à XXL)
(3, 1, 5), (3, 2, 15), (3, 3, 22), (3, 4, 20), (3, 5, 15), (3, 6, 8),
-- Venum Elite (Combat - 8-16)
(4, 2, 12), (4, 3, 28), (4, 4, 35), (4, 5, 22), (4, 6, 8),
-- Everlast PowerLock (Combat - 8-14)
(5, 2, 15), (5, 3, 25), (5, 4, 30), (5, 5, 20),
-- Venum Impact MMA (Combat - S-L)
(6, 2, 30), (6, 3, 45), (6, 4, 35),
-- Everlast Pro Style (Combat - 8-16)
(7, 2, 30), (7, 3, 50), (7, 4, 55), (7, 5, 35), (7, 6, 15),
-- The North Face Etip (Hiver - XS à XL)
(8, 1, 10), (8, 2, 25), (8, 3, 35), (8, 4, 30), (8, 5, 15),
-- Columbia Thermarator (Hiver - S à XXL)
(9, 2, 30), (9, 3, 45), (9, 4, 40), (9, 5, 25), (9, 6, 12),
-- The North Face Montana (Hiver - XS à XL)
(10, 1, 8), (10, 2, 20), (10, 3, 28), (10, 4, 25), (10, 5, 14),
-- Columbia Whirlibird (Hiver - S à XL)
(11, 2, 22), (11, 3, 35), (11, 4, 32), (11, 5, 18),
-- Rostaing Jardin Expert (Jardinage - S à XL)
(12, 2, 40), (12, 3, 60), (12, 4, 55), (12, 5, 30),
-- Mapa Jardin Pro (Jardinage - M à XXL)
(13, 3, 50), (13, 4, 70), (13, 5, 45), (13, 6, 20),
-- Rostaing Rosier (Jardinage - S à XL)
(14, 2, 35), (14, 3, 55), (14, 4, 50), (14, 5, 28),
-- Mechanix Garden (Jardinage - S à XXL)
(15, 2, 30), (15, 3, 48), (15, 4, 45), (15, 5, 32), (15, 6, 15),
-- Rossignol Ski (Ski - XS à XL)
(16, 1, 6), (16, 2, 18), (16, 3, 25), (16, 4, 22), (16, 5, 12),
-- The North Face Apex (Ski - XS à XL)
(17, 1, 5), (17, 2, 15), (17, 3, 22), (17, 4, 20), (17, 5, 10),
-- Rossignol Tempest (Ski - S à XL)
(18, 2, 12), (18, 3, 20), (18, 4, 18), (18, 5, 8),
-- Mechanix Original (Protection - S à XXL)
(19, 2, 35), (19, 3, 55), (19, 4, 50), (19, 5, 30), (19, 6, 15),
-- Mechanix M-Pact (Protection - S à XL)
(20, 2, 28), (20, 3, 45), (20, 4, 42), (20, 5, 25);

-- COMMANDES
INSERT INTO commande VALUES
(1, '2025-01-15 10:30:00', 2, 'U001'),
(2, '2025-01-16 14:20:00', 2, 'U002'),
(3, '2025-01-17 09:15:00', 1, 'U004'),
(4, '2025-01-18 16:45:00', 1, 'U005'),
(5, '2025-01-19 11:00:00', 2, 'U001'),
(6, '2025-01-20 13:30:00', 1, 'U002');

-- LIGNES DE COMMANDE
INSERT INTO ligne_commande VALUES
-- Commande 1 (Vélo + Hiver)
(1, 1, 1, 39.99),
(1, 8, 1, 49.99),
-- Commande 2 (Jardinage)
(2, 12, 2, 14.99),
(2, 13, 3, 12.99),
-- Commande 3 (Combat + Protection)
(3, 4, 1, 119.99),
(3, 19, 2, 24.99),
-- Commande 4 (Ski)
(4, 16, 1, 79.99),
(4, 17, 1, 89.99),
-- Commande 5 (Vélo + Combat)
(5, 3, 1, 54.99),
(5, 6, 1, 69.99),
-- Commande 6 (Hiver + Jardinage)
(6, 10, 1, 69.99),
(6, 14, 2, 18.99);

-- PANIERS EN COURS
INSERT INTO ligne_panier VALUES
('U001', 2, 1, '2025-01-21'),
('U001', 15, 1, '2025-01-21'),
('U002', 5, 1, '2025-01-22'),
('U004', 9, 2, '2025-01-20'),
('U004', 20, 1, '2025-01-20'),
('U005', 18, 1, '2025-01-22');

-- ============================================
-- STATISTIQUES DU JEU DE DONNÉES
-- ============================================
-- 20 articles (gants variés)
-- 6 types d'articles : Vélo (3), Sport Combat (4), Hiver (4), Jardinage (4), Ski (3), Protection (2)
-- 10 marques variées
-- 5 fournisseurs spécialisés
-- 10 couleurs
-- 6 tailles
-- 6 utilisateurs (dont 1 admin, 1 vendeur)
-- 6 commandes avec états "En attente" ou "Expédiée"
-- 12 lignes de commande
-- 6 articles dans les paniers en cours
-- Stock total : environ 2100 pièces
-- ============================================
