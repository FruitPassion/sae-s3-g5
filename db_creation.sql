CREATE OR REPLACE USER 'local_user'@'localhost' IDENTIFIED BY 'password';
DROP DATABASE IF EXISTS db_fiches_dev;
create database db_fiches_dev;
grant all privileges on db_fiches_dev.* TO 'local_user'@'localhost' identified by 'password';
flush privileges;
USE db_fiches_dev;

CREATE TABLE Personnel(
   id_personnel INT AUTO_INCREMENT,
   nom VARCHAR(50) NOT NULL,
   prenom VARCHAR(50) NOT NULL,
   login VARCHAR(50) NOT NULL,
   mdp TEXT,
   role VARCHAR(50),
   PRIMARY KEY(id_personnel)
   CONSTRAINT ch_personnel_role CHECK (role IN ('SuperAdministrateur', 'Educateur Administrateur', 'Educateur', 'CIP'))
);

CREATE TABLE Apprenti(
   id_apprenti INT AUTO_INCREMENT,
   nom VARCHAR(50) NOT NULL,
   prenom VARCHAR(50) NOT NULL,
   login VARCHAR(50),
   mdp TEXT,
   photo VARCHAR(100),
   PRIMARY KEY(id_apprenti)
);

CREATE TABLE Formation(
   id_formation INT AUTO_INCREMENT,
   intitule VARCHAR(100) NOT NULL,
   niveau_qualif VARCHAR(25),
   groupe INT,
   PRIMARY KEY(id_formation)
);

CREATE TABLE Session(
   id_session INT AUTO_INCREMENT,
   theme VARCHAR(50),
   cours VARCHAR(50),
   duree INT,
   id_formation INT NOT NULL,
   PRIMARY KEY(id_session),
   FOREIGN KEY(id_formation) REFERENCES Formation(id_formation)
);

CREATE TABLE EducAdmin(
   id_personnel INT,
   PRIMARY KEY(id_personnel),
   FOREIGN KEY(id_personnel) REFERENCES Personnel(id_personnel)
);

CREATE TABLE Pictogramme(
   id_pictogramme INT AUTO_INCREMENT,
   label VARCHAR(50),
   url VARCHAR(100),
   categorie VARCHAR(50),
   PRIMARY KEY(Id_Pictogramme)
);

CREATE TABLE ElementDefaut(
   id_element INT AUTO_INCREMENT,
   type VARCHAR(50),
   text VARCHAR(50),
   audio VARCHAR(50),
   Id_Pictogramme INT NOT NULL,
   id_personnel INT NOT NULL,
   PRIMARY KEY(id_element),
   FOREIGN KEY(id_pictogramme) REFERENCES Pictogramme(id_pictogramme),
   FOREIGN KEY(id_personnel) REFERENCES EducAdmin(id_personnel)
);

CREATE TABLE FicheIntervention(
   id_fiche INT AUTO_INCREMENT,
   numero SMALLINT,
   nom_du_demandeur VARCHAR(50),
   date_demande DATE,
   date_intervention DATE,
   duree_intervention VARCHAR(50),
   localisation VARCHAR(50),
   description_demande TEXT,
   degre_urgence VARCHAR(50),
   type_intervention VARCHAR(50),
   nature_intervention VARCHAR(50),
   couleur_intervention VARCHAR(50),
   etat_fiche VARCHAR(50),
   date_creation DATETIME,
   id_personnel INT NOT NULL,
   id_apprenti INT NOT NULL,
   PRIMARY KEY(id_fiche),
   FOREIGN KEY(id_apprenti) REFERENCES Apprenti(id_apprenti),
   FOREIGN KEY(id_personnel) REFERENCES EducAdmin(id_personnel)
);

CREATE TABLE Trace(
   id_personnel INT,
   horodatage DATETIME,
   intitule VARCHAR(50),
   eval_texte TEXT,
   commentaire_texte TEXT,
   eval_audio VARCHAR(255),
   commentaire_audio VARCHAR(50),
   id_fiche INT NOT NULL,
   PRIMARY KEY(id_personnel, horodatage),
   FOREIGN KEY(id_personnel) REFERENCES Personnel(id_personnel),
   FOREIGN KEY(id_fiche) REFERENCES FicheIntervention(id_fiche)
);

CREATE TABLE Assister(
   id_apprenti INT,
   id_session INT,
   PRIMARY KEY(id_apprenti, id_session),
   FOREIGN KEY(id_apprenti) REFERENCES Apprenti(id_apprenti),
   FOREIGN KEY(id_session) REFERENCES Session(id_session)
);

CREATE TABLE Composer(
   id_element INT,
   id_fiche INT,
   picto VARCHAR(50),
   text VARCHAR(50),
   taille_texte VARCHAR(50),
   police VARCHAR(50),
   audio VARCHAR(50),
   couleur VARCHAR(50),
   couleur_fond VARCHAR(50),
   niveau TINYINT,
   PRIMARY KEY(id_element, id_fiche),
   FOREIGN KEY(id_element) REFERENCES ElementDefaut(id_element),
   FOREIGN KEY(id_fiche) REFERENCES FicheIntervention(id_fiche)
);

INSERT INTO Apprenti (nom, prenom, login)
VALUES ('Jacquard', 'Davy', 'DAJ12'),
       ('Guilbert', 'Ange', 'ANG12'),
       ('Poussin', 'Christian', 'CHP14'),
       ('Trouvé', 'Éloi', 'ELT10'),
       ('Cordonnier', 'Danny', 'DAC15'),
       ('Massé', 'Xavier', 'XAM11'),
       ('Meissa', 'Abdelkhader', 'ABM17');

INSERT INTO Personnel (nom, prenom, login, role)
VALUES ('Dupont', 'Jean', 'JED10', 'SuperAdministrateur'),
       ('Lamar', 'Allain', 'ALL11', 'Educateur Administrateur'),
       ('DitCharo', 'Mathieu', 'MAD14', 'Educateur Administrateur'),
       ('Oskour', 'Jeanne', 'JEO12', 'Educateur'),
       ('Curry', 'Marie', 'MAC10', 'Educateur'),
       ('Barre', 'Lenny', 'LEB08', 'Educateur'),
       ('Zirot', 'Benoit', 'BEZ11', 'Educateur'),
       ('Rouselle', 'Fabienne', 'FAR16', 'CIP');

INSERT INTO Formation (intitule, niveau_qualif, groupe)
VALUES ('Parcour plomberie','CAP',1),
       ('Agent de maintenance en bâtiment','Licence',2);


