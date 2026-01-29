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

CREATE TABLE taille(
   id_taille INT,
   num_taille_fr VARCHAR(50),
   taille_us VARCHAR(50),
   tour_de_main VARCHAR(50),
   PRIMARY KEY(id_taille)
);

CREATE TABLE type_gant(
   id_type_gant INT,
   nom_type_gant VARCHAR(255),
   PRIMARY KEY(id_type_gant)
);

CREATE TABLE commande(
   id_commande INT,
   date_achat DATETIME,
   etat_id INT NOT NULL,
   utilisateur_id VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
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
   type_gant_id INT NOT NULL,
   taille_id INT NOT NULL,
   PRIMARY KEY(id_gant),
   FOREIGN KEY(type_gant_id) REFERENCES type_gant(id_type_gant),
   FOREIGN KEY(taille_id) REFERENCES taille(id_taille)
);

CREATE TABLE ligne_commande(
   commande_id INT,
   gant_id INT,
   quantite INT,
   prix DECIMAL(19,4),
   PRIMARY KEY(commande_id, gant_id),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
   FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
);

CREATE TABLE ligne_panier(
   utilisateur_id VARCHAR(50),
   gant_id INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(utilisateur_id, gant_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(gant_id) REFERENCES gant(id_gant)
);