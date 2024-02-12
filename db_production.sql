-- Active: 1706110255136@@127.0.0.1@3306@db_fiches_dev

USE db_fiches_prod;


CREATE TABLE Personnel
(
    id_personnel INT AUTO_INCREMENT,
    nom          VARCHAR(50) NOT NULL,
    prenom       VARCHAR(50) NOT NULL,
    login        VARCHAR(50) NOT NULL,
    mdp          TEXT        NOT NULL,
    role         VARCHAR(50) NOT NULL,
    email        VARCHAR(100),
    essais      INT         NOT NULL DEFAULT (0),
    archive      BOOLEAN     NOT NULL DEFAULT (0),
    PRIMARY KEY (id_personnel),
    CONSTRAINT ch_personnel_role CHECK (role IN
                                        ('SuperAdministrateur', 'Educateur Administrateur', 'Educateur', 'CIP', 'dummy')),
    CONSTRAINT ch_personnel_essais CHECK (Personnel.essais >= 0 AND Personnel.essais <= 3)
);

CREATE TABLE Apprenti
(
    id_apprenti INT AUTO_INCREMENT,
    nom         VARCHAR(50) NOT NULL,
    prenom      VARCHAR(50) NOT NULL,
    login       VARCHAR(50) NOT NULL,
    mdp         TEXT,
    photo       VARCHAR(100),
    essais     INT         NOT NULL DEFAULT (0),
    archive     BOOLEAN     NOT NULL DEFAULT (0),
    adaptation_situation_examen TEXT,
    PRIMARY KEY (id_apprenti),
    CONSTRAINT ch_apprenti_essais CHECK (Apprenti.essais >= 0 AND Apprenti.essais <= 5)
);

CREATE TABLE Formation
(
    id_formation  INT AUTO_INCREMENT,
    intitule      VARCHAR(50) NOT NULL,
    niveau_qualif SMALLINT    NOT NULL,
    groupe        VARCHAR(50),
    image         VARCHAR(100),
    archive       BOOLEAN     NOT NULL DEFAULT (0),
    PRIMARY KEY (id_formation)
);

CREATE TABLE Cours
(
    id_cours   INT AUTO_INCREMENT,
    theme        VARCHAR(50) NOT NULL,
    cours        VARCHAR(50) NOT NULL,
    duree        INT,
    id_formation INT         NOT NULL,
    archive      BOOLEAN     NOT NULL DEFAULT (0),
    PRIMARY KEY (id_cours),
    FOREIGN KEY (id_formation) REFERENCES Formation (id_formation)
);

CREATE TABLE EducAdmin
(
    id_personnel INT,
    PRIMARY KEY (id_personnel),
    FOREIGN KEY (id_personnel) REFERENCES Personnel (id_personnel)
);

CREATE TABLE Pictogramme
(
    id_pictogramme INT AUTO_INCREMENT,
    label          VARCHAR(50),
    url            VARCHAR(100),
    categorie      VARCHAR(50),
    souscategorie  VARCHAR(50),
    PRIMARY KEY (id_pictogramme)
);

CREATE TABLE ElementBase
(
    id_element   INT AUTO_INCREMENT,
    libelle      VARCHAR(50) NOT NULL,
    type         VARCHAR(50) NOT NULL,
    text         VARCHAR(50),
    audio        VARCHAR(100),
    PRIMARY KEY (id_element)
);

CREATE TABLE FicheIntervention
(
    id_fiche             INT AUTO_INCREMENT,
    numero               SMALLINT,
    nom_du_demandeur     VARCHAR(50),
    date_demande         DATE,
    localisation         VARCHAR(50),
    description_demande  TEXT,
    degre_urgence        TINYINT,
    couleur_intervention VARCHAR(50),
    etat_fiche           TINYINT,
    date_creation        DATETIME,
    photo_avant          VARCHAR(150),
    photo_apres          VARCHAR(150),
    nom_intervenant      VARCHAR(50) NOT NULL,
    prenom_intervenant   VARCHAR(50) NOT NULL,
    id_personnel         INT         NOT NULL,
    id_apprenti          INT         NOT NULL,
    id_cours         INT         NOT NULL,
    PRIMARY KEY (id_fiche),
    FOREIGN KEY (id_personnel) REFERENCES EducAdmin (id_personnel),
    FOREIGN KEY (id_apprenti) REFERENCES Apprenti (id_apprenti),
    FOREIGN KEY (id_cours) REFERENCES Cours (id_cours),
    CONSTRAINT ch_fiche_etat CHECK (FicheIntervention.etat_fiche >= 0 AND FicheIntervention.etat_fiche <= 2),
    CONSTRAINT ch_fiche_degre CHECK (FicheIntervention.degre_urgence >= 1 AND FicheIntervention.degre_urgence <= 4)
);

CREATE TABLE LaisserTrace
(
    id_personnel      INT,
    horodatage        DATETIME,
    intitule          VARCHAR(50) NOT NULL,
    eval_texte        TEXT        NOT NULL,
    commentaire_texte TEXT        NOT NULL,
    eval_audio        VARCHAR(255),
    commentaire_audio VARCHAR(50),
    apprenti          BOOLEAN,
    id_fiche          INT         NOT NULL,
    PRIMARY KEY (id_personnel, horodatage),
    FOREIGN KEY (id_personnel) REFERENCES Personnel (id_personnel),
    FOREIGN KEY (id_fiche) REFERENCES FicheIntervention (id_fiche),
    CONSTRAINT uc_commentaire_fiche UNIQUE (id_fiche, apprenti)

);



CREATE TABLE Assister
(
    id_apprenti INT,
    id_cours  INT,
    PRIMARY KEY (id_apprenti, id_cours),
    FOREIGN KEY (id_apprenti) REFERENCES Apprenti (id_apprenti),
    FOREIGN KEY (id_cours) REFERENCES Cours (id_cours)
);


CREATE TABLE Materiel
(
    id_materiel INT AUTO_INCREMENT,
    nom         VARCHAR(50) NOT NULL,
    categorie   VARCHAR(50) NOT NULL,
    lien       VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_materiel)
);

CREATE TABLE ComposerPresentation
(
    id_element          INT,
    id_fiche            INT,
    text                VARCHAR(50),
    taille_texte        VARCHAR(50),
    audio               VARCHAR(50),
    police              VARCHAR(50),
    couleur             VARCHAR(7),
    couleur_fond        VARCHAR(7),
    niveau              TINYINT,
    position_elem       VARCHAR(50),
    ordre_saisie_focus  VARCHAR(50),
    id_pictogramme      INT,
    taille_pictogramme  INT,
    couleur_pictogramme VARCHAR(7),
    id_materiel         INT,
    PRIMARY KEY (id_element, id_fiche),
    FOREIGN KEY (id_element) REFERENCES ElementBase (id_element),
    FOREIGN KEY (id_fiche) REFERENCES FicheIntervention (id_fiche),
    FOREIGN KEY (id_pictogramme) REFERENCES Pictogramme (id_pictogramme)
);


INSERT INTO Personnel (nom, prenom, login, mdp, role, email, essais)
VALUES ('Supprimé', 'Utilisateur', 'dummy', 'dummy', 'dummy', NULL, 3),
       ('--AREMPLACERNOM--', '--AREMPLACERPRENOM--', '--AREMPLACERLOG--', '--AREMPLACERMDP--', 'SuperAdministrateur', '--AREMPLACERMAIL--', 0);



INSERT INTO Apprenti (nom, prenom, mdp, login, photo, essais, adaptation_situation_examen)
VALUES ('dummy', 'dummy', 'dummy', 'dummy', 'dummy', 0, null);


INSERT INTO ElementBase (libelle, type, text, audio)
VALUES ('Intervention', 'categorie', NULL, NULL),
       ('Date de l\'intervention', 'date', NULL, NULL),
       ('Durée de l\'opération', 'select-time', NULL, NULL),
       ('Confirmation des informations', 'checkbox', NULL, NULL),
       ('Type de Maintenance', 'categorie', NULL, NULL),
       ('améliorative', 'checkbox', NULL, NULL),
       ('préventive', 'checkbox', NULL, NULL),
       ('corrective', 'checkbox', NULL, NULL),
       ('Nature de l\'intervention', 'categorie', NULL, NULL),
       ('Aménagement', 'checkbox', NULL, NULL),
       ('Finitions', 'checkbox', NULL, NULL),
       ('Installation sanitaire', 'checkbox', NULL, NULL),
       ('Installation électrique', 'checkbox', NULL, NULL),
       ('Description du travail', 'categorie', NULL, NULL),
       ('Travaux réalisés', 'textarea', NULL, NULL),
       ('Travaux non réalisé', 'textarea', NULL, NULL),
       ('Nécessite une nouvelle intervention', 'checkbox', NULL, NULL),
       ('Matériaux utilisés', 'categorie', NULL, NULL),
       ('Materiel 1', 'select-materiel', NULL, NULL),
       ('Materiel 2', 'select-materiel', NULL, NULL),
       ('Materiel 3', 'select-materiel', NULL, NULL),
       ('Materiel 4', 'select-materiel', NULL, NULL),
       ('Materiel 5', 'select-materiel', NULL, NULL),
       ('Materiel 6', 'select-materiel', NULL, NULL),
       ('Materiel 7', 'select-materiel', NULL, NULL),
       ('Materiel 8', 'select-materiel', NULL, NULL),
       ('Materiel 9', 'select-materiel', NULL, NULL),
       ('Materiel 10', 'select-materiel', NULL, NULL),
       ('Ressenti','categorie',NULL,NULL),
       ('Très mauvais','radio',NULL,NULL),
       ('Mauvais','radio',NULL,NULL),
       ('Moyen','radio',NULL,NULL),
       ('Assez bien','radio',NULL,NULL),
       ('Bien','radio',NULL,NULL);

INSERT INTO FicheIntervention (id_fiche, numero, nom_du_demandeur, date_demande, localisation, description_demande,
                               degre_urgence, couleur_intervention, etat_fiche, date_creation, id_personnel,
                               id_apprenti, nom_intervenant, prenom_intervenant, id_cours)
VALUES (1, 0, 'dummy', '1990-01-01', 'dummy', 'dummy', 4, 'vert', 0, '1999-01-01 01:01:01', 3, 1, 'Daniel', 'Bernard', 1);


INSERT INTO ComposerPresentation (id_element, id_fiche, taille_texte, audio, police, couleur, couleur_fond,
                                  niveau, position_elem, ordre_saisie_focus, id_pictogramme, taille_pictogramme,
                                  couleur_pictogramme, id_materiel)
VALUES (1, 1, 20, NULL, 'Montserrat', '#000000', '#FFFFFF', NULL, '10', NULL, NULL, 10, '#000000', NULL),
       (2, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '11', NULL, 3, 10, '#000000', NULL),
       (3, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '12', NULL, 11, 10, '#000000', NULL),
       (4, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '13', NULL, 9, 10, '#000000', NULL),
       (5, 1, 20, NULL, 'Montserrat', '#000000', '#FFFFFF', NULL, '20', NULL, NULL, 10, '#000000', NULL),
       (6, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '21', NULL, 2, 10, '#000000', NULL),
       (7, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '22', NULL, 17, 10, '#000000', NULL),
       (8, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '23', NULL, 4, 10, '#000000', NULL),
       (9, 1, 20, NULL, 'Montserrat', '#000000', '#FFFFFF', NULL, '30', NULL, NULL, 10, '#000000', NULL),
       (10, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '31', NULL, 12, 10, '#000000', NULL),
       (11, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '32', NULL, 13, 10, '#000000', NULL),
       (12, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '33', NULL, 14, 10, '#000000', NULL),
       (13, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '34', NULL, 18, 10, '#000000', NULL),
       (14, 1, 20, NULL, 'Montserrat', '#000000', '#FFFFFF', 1, '40', NULL, NULL, 10, '#000000', NULL),
       (15, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '41', NULL, 10, 10, '#000000', NULL),
       (16, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '42', NULL, 7, 10, '#000000', NULL),
       (17, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '43', NULL, 21, 10, '#000000', NULL),
       (18, 1, 20, NULL, 'Montserrat', '#000000', '#FFFFFF', NULL, '50', NULL, 20, 10, '#000000', NULL),
       (19, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '51', NULL, 20, 10, '#000000', 1),
       (20, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '52', NULL, 20, 10, '#000000', 2),
       (21, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '53', NULL, 20, 10, '#000000', 3),
       (22, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '54', NULL, 20, 10, '#000000', 3),
       (23, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '55', NULL, 20, 10, '#000000', 1),
       (24, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '56', NULL, 20, 10, '#000000', 1),
       (25, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '57', NULL, 20, 10, '#000000', 1),
       (26, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '58', NULL, 20, 10, '#000000', 1),
       (27, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '59', NULL, 20, 10, '#000000', 1),
       (28, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '510', NULL, 20, 10, '#000000', 1),
       (29, 1, 20, NULL, 'Montserrat', '#000000', '#FFFFFF', NULL, '60', NULL, 20, 10, '#000000', NULL),
       (30, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '61', NULL, 26, 10, '#000000', NULL),
       (31, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '62', NULL, 25, 10, '#000000', NULL),
       (32, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '63', NULL, 24, 10, '#000000', NULL),
       (33, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '64', NULL, 23, 10, '#000000', NULL),
       (34, 1, 20, NULL, 'Montserrat', '#000000', NULL, 1, '65', NULL, 22, 10, '#000000', NULL);


INSERT INTO Materiel (nom, lien, categorie)
VALUES ('Cable de terre', 'elec/cable_terre.jpg', 'Electrique'),
       ('Denudeur de cables', 'elec/denuder_cable.jpg', 'Electrique'),
       ('Multimetre', 'elec/multimetre.jpg', 'Electrique'),
       ('Multiprise', 'elec/multiprise.jpg', 'Electrique'),
       ('Pince à dénuder', 'elec/pince_denuder.jpg', 'Electrique'),
       ('Pince universelle isolée', 'elec/pince_universelle_isolee.jpg', 'Electrique'),
       ('Tournevis électriques', 'elec/tournevis_elec.jpg', 'Electrique'),
       ('Chalumeau 1', 'plomb/chalumeau1.jpg', 'Plomberie'),
       ('Chalumeau 2', 'plomb/chalumeau2.jpg', 'Plomberie'),
       ('Clée à molette', 'plomb/cle_molette.jpg', 'Plomberie'),
       ('Coupe tube cuivre', 'plomb/coupe_tube_cuivre.jpg', 'Plomberie'),
       ('Coupe tube PVC', 'plomb/coupe_tube_pvc.jpg', 'Plomberie'),
       ('Emboiture', 'plomb/emboiture.jpg', 'Plomberie'),
       ('Molette Virax', 'plomb/molette_virax.jpg', 'Plomberie'),
       ('Pince multiprises', 'plomb/molette_virax.jpg', 'Plomberie'),
       ('Beton', 'general/beton.jpg', 'General'),
       ('Chevilles molly', 'general/chevilles_molly.jpg', 'General'),
       ('Chevilles plastique', 'general/chevilles_plastiques.jpg', 'General'),
       ('Crampon','general/crampon.jpg', 'General'),
       ('Marteau','general/marteau.jpg', 'General'),
       ('Metal','general/metal.png', 'General'),
       ('Metre','general/metre.jpg', 'General'),
       ('Niveau','general/niveau.jpg', 'General'),
       ('Perfo','general/perfo.jpg', 'General'),
       ('Pince à chevilles molly','general/pince_chevilles_molly.jpg', 'General'),
       ('Tournevis cruciforme', 'general/tournevis_cruciforme.jpg', 'General'),
        ('Tournevis plat', 'general/tournevis_plat.jpg', 'General'),
        ('Tournevis','general/tournevis.jpg', 'General'),
        ('Visseuse','general/visseuse.jpg', 'General');

INSERT INTO Pictogramme (label, url, categorie, souscategorie)
VALUES ('Ajouter', 'ajouter.png', 'Matériaux utilisés', 'ajouter'),
       ('Ameliorative', 'amelioratif.png', 'Type de Maintenance', 'ameliorative'),
       ('Calendrier', 'calendrier.png', 'Intervention', 'calendrier'),
       ('Corrective', 'corrective.png', 'Type de Maintenance', 'corrective'),
       ('Demande', 'demande.png', 'Autre', NULL),
       ('Eclair', 'eclair.png', 'Autre', NULL),
       ('Sablier', 'en-cours.png', 'Description du travail', 'non réalisés'),
       ('Annuler', 'annuler.png', 'Autre', NULL),
       ('Fini', 'fini.png', 'Intervention', 'fini'),
       ('Finis', 'finis.png', 'Description du travail', 'réalisés'),
       ('Horloge', 'horloge.png', 'Intervention', 'horloge'),
       ('Ammenagement', 'ammenagement.png', 'Nature Intervention', 'ammenagement'),
       ('Finitions', 'finitions.png', 'Nature Intervention', 'finitions'),
       ('Sanitaires', 'sanitaires.png', 'Nature Intervention', 'sanitaires'),
       ('Lieu', 'lieu.png', 'Autre', NULL),
       ('Modifier', 'modifier.png', 'Autre', NULL),
       ('Preventive', 'preventive.png', 'Type de Maintenance', 'preventive'),
       ('Prise', 'prise.png', 'Nature Intervention', 'electrique'),
       ('Valider', 'valider.png', 'Autre', NULL),
       ('Materiel', 'materiel.png', 'Matériaux utilisés', 'choix materiel'),
       ('Nouvelle', 'nouvelle.png', 'Description du travail', 'nouvelle'),
       ('Bien','bien.png','Ressenti','tres bien'),
       ('Assez bien','assez_bien.png','Ressenti','bien'),
       ('Moyen','moyen.png','Ressenti','assez bien'),
       ('Mauvais','mauvais.png','Ressenti','moyen'),
       ('Très mauvais','tres_mauvais.png','Ressenti','pas bien');