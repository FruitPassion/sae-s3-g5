CREATE OR REPLACE USER 'local_user'@'localhost' IDENTIFIED BY 'password';
DROP DATABASE IF EXISTS db_fiches_dev;
create database db_fiches_dev;
grant all privileges on db_fiches_dev.* TO 'local_user'@'localhost' identified by 'password';
flush privileges;
USE db_fiches_dev;

CREATE TABLE Formation(
   Id_Formation INT AUTO_INCREMENT,
   Intitule VARCHAR(100) NOT NULL,
   NiveauQualif VARCHAR(25) NOT NULL,
   PRIMARY KEY(Id_Formation)
);

CREATE TABLE Session(
   Id_Session INT AUTO_INCREMENT,
   Theme VARCHAR(25) NOT NULL,
   Cours VARCHAR(50) NOT NULL,
   Debut DATE NOT NULL,
   Duree DATE NOT NULL,
   PRIMARY KEY(Id_Session)
);

CREATE TABLE Apprenti(
   Id_Apprenti INT AUTO_INCREMENT,
   Nom VARCHAR(50) NOT NULL,
   Prenom VARCHAR(50) NOT NULL,
   Login VARCHAR(50) NOT NULL,
   MDP INT,
   Id_Formation INT NOT NULL,
   PRIMARY KEY(Id_Apprenti),
   FOREIGN KEY(Id_Formation) REFERENCES Formation(Id_Formation)
);

CREATE TABLE ElementForm(
   Id_ElementForm INT AUTO_INCREMENT,
   TypeElt VARCHAR(50) NOT NULL,
   Picto VARCHAR(100),
   Libelle VARCHAR(100) NOT NULL,
   Audio VARCHAR(100),
   TailleLibelle INT NOT NULL,
   PoliceLibelle VARCHAR(50) NOT NULL,
   CouleurLibelle CHAR(6) NOT NULL,
   CouleurFondLib CHAR(6) NOT NULL,
   NiveauAffichage TINYINT NOT NULL,
   DateHeure DATETIME NOT NULL,
   ReponseApprenti TEXT,
   PRIMARY KEY(Id_ElementForm)
);

CREATE TABLE Personnel(
   Id_Personnel INT AUTO_INCREMENT,
   Nom VARCHAR(50) NOT NULL,
   Prenom VARCHAR(50) NOT NULL,
   Login VARCHAR(50) NOT NULL,
   MDP VARCHAR(50) NOT NULL,
   Role VARCHAR(50) NOT NULL,
   PRIMARY KEY(Id_Personnel)
);

CREATE TABLE Intervention(
   Id_Intervention INT AUTO_INCREMENT,
   DateIntervention DATE NOT NULL,
   TypeIntervention VARCHAR(50) NOT NULL,
   NatureIntervention VARCHAR(50) NOT NULL,
   PRIMARY KEY(Id_Intervention)
);

CREATE TABLE Archiver(
   Id_Apprenti INT,
   Date_archive DATETIME,
   O_N BOOLEAN NOT NULL,
   Id_Personnel INT NOT NULL,
   PRIMARY KEY(Id_Apprenti, Date_archive),
   UNIQUE(Id_Apprenti),
   FOREIGN KEY(Id_Apprenti) REFERENCES Apprenti(Id_Apprenti),
   FOREIGN KEY(Id_Personnel) REFERENCES Personnel(Id_Personnel)
);

CREATE TABLE Fiche(
   Id_Fiche INT AUTO_INCREMENT,
   NumFiche INT NOT NULL,
   NomDemandeur VARCHAR(50) NOT NULL,
   DateDemande DATE NOT NULL,
   Localisation VARCHAR(100) NOT NULL,
   Description TEXT NOT NULL,
   DegreUrgence INT NOT NULL,
   EtatFicheApprenti VARCHAR(50) NOT NULL,
   Id_Apprenti INT NOT NULL,
   Id_Intervention INT NOT NULL,
   Id_Session INT NOT NULL,
   PRIMARY KEY(Id_Fiche),
   FOREIGN KEY(Id_Apprenti) REFERENCES Apprenti(Id_Apprenti),
   FOREIGN KEY(Id_Intervention) REFERENCES Intervention(Id_Intervention),
   FOREIGN KEY(Id_Session) REFERENCES Session(Id_Session)
);

CREATE TABLE Trace(
   Id_Fiche INT,
   DateFinFiche DATETIME,
   EvalTextuelle TEXT NOT NULL,
   Intitule VARCHAR(50) NOT NULL,
   EvalAudio VARCHAR(100),
   CommentaireTextuel TEXT NOT NULL,
   CommentaireAudio VARCHAR(100),
   Id_Personnel INT NOT NULL,
   PRIMARY KEY(Id_Fiche, DateFinFiche),
   FOREIGN KEY(Id_Fiche) REFERENCES Fiche(Id_Fiche),
   FOREIGN KEY(Id_Personnel) REFERENCES Personnel(Id_Personnel)
);

CREATE TABLE Avoir(
   Id_ElementForm INT,
   Id_Fiche INT,
   PRIMARY KEY(Id_ElementForm, Id_Fiche),
   FOREIGN KEY(Id_ElementForm) REFERENCES ElementForm(Id_ElementForm),
   FOREIGN KEY(Id_Fiche) REFERENCES Fiche(Id_Fiche)
);

CREATE TABLE Responsable(
   Id_Formation INT,
   Id_Personnel INT,
   PRIMARY KEY(Id_Formation, Id_Personnel),
   FOREIGN KEY(Id_Formation) REFERENCES Formation(Id_Formation),
   FOREIGN KEY(Id_Personnel) REFERENCES Personnel(Id_Personnel)
);

INSERT INTO Personnel (Nom, Prenom, Login, MDP, Role)
VALUES ('Lamar', 'Allain', 'LAA34', 'mdp23434', 'Educateur'),
       ('Dupont', 'Jean', 'DUJ14', 'smlksfpof', 'Administrateur');
