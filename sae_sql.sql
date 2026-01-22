DROP TABLE IF EXISTS est_de_taille;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS gant;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur(
   id_utilisateur VARCHAR(50),
   login VARCHAR(50),
   email VARCHAR(50),
   nom_utilisateur VARCHAR(50),
   password VARCHAR(255),
   role VARCHAR(50),
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE etat(
   id_etat INT,
   libelle_etat VARCHAR(50),
   PRIMARY KEY(id_etat)
);

CREATE TABLE gant(
   id_gant INT,
   nom_gant VARCHAR(50),
   poids INT,
   couleur VARCHAR(50),
   prix_gant DECIMAL(19,4),
   photo VARCHAR(50),
   founisseur VARCHAR(50),
   marque VARCHAR(50),
   stock VARCHAR(50),
   PRIMARY KEY(id_gant)
);

CREATE TABLE taille(
   id_taille INT,
   num_taille_fr VARCHAR(50),
   taille_us VARCHAR(50),
   tour_de_main VARCHAR(50),
   PRIMARY KEY(id_taille)
);

CREATE TABLE commande(
   id_commande INT,
   date_achat DATETIME,
   id_etat INT NOT NULL,
   id_utilisateur VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ligne_commande(
   id_commande INT,
   id_gant INT,
   quantite INT,
   prix DECIMAL(19,4),
   PRIMARY KEY(id_commande, id_gant),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant)
);

CREATE TABLE ligne_panier(
   id_utilisateur VARCHAR(50),
   id_gant INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_utilisateur, id_gant),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant)
);

CREATE TABLE est_de_taille(
   id_gant INT,
   id_taille INT,
   PRIMARY KEY(id_gant, id_taille),
   FOREIGN KEY(id_gant) REFERENCES gant(id_gant),
   FOREIGN KEY(id_taille) REFERENCES taille(id_taille)
);
