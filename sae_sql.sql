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
