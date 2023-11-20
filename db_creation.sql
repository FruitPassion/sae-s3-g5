CREATE OR REPLACE USER 'local_user'@'localhost' IDENTIFIED BY 'password';
DROP DATABASE IF EXISTS db_fiches_dev;
create database db_fiches_dev;
grant all privileges on db_fiches_dev.* TO 'local_user'@'localhost' identified by 'password';
flush privileges;
USE db_fiches_dev;


CREATE TABLE Personnel
(
    id_personnel INT AUTO_INCREMENT,
    nom          VARCHAR(50) NOT NULL,
    prenom       VARCHAR(50) NOT NULL,
    login        VARCHAR(50) NOT NULL,
    mdp          TEXT        NOT NULL,
    role         VARCHAR(50),
    PRIMARY KEY (id_personnel),
    CONSTRAINT ch_personnel_role CHECK (role IN ('SuperAdministrateur', 'Educateur Administrateur', 'Educateur', 'CIP'))
);

CREATE TABLE Apprenti
(
    id_apprenti INT AUTO_INCREMENT,
    nom         VARCHAR(50) NOT NULL,
    prenom      VARCHAR(50) NOT NULL,
    login       VARCHAR(50) NOT NULL,
    mdp         TEXT NOT NULL,
    photo       VARCHAR(100),
    PRIMARY KEY (id_apprenti)
);

CREATE TABLE Formation
(
    id_formation  INT AUTO_INCREMENT,
    intitule      VARCHAR(50) NOT NULL,
    niveau_qualif SMALLINT,
    groupe        VARCHAR(50),
    image         VARCHAR(100),
    PRIMARY KEY (id_formation)
);

CREATE TABLE Session
(
    id_session   INT AUTO_INCREMENT,
    theme        VARCHAR(50) NOT NULL,
    cours        VARCHAR(50) NOT NULL,
    duree        INT,
    id_formation INT NOT NULL,
    PRIMARY KEY (id_session),
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
    PRIMARY KEY (id_pictogramme)
);

CREATE TABLE ElementDefaut
(
    id_element     INT AUTO_INCREMENT,
    libelle        VARCHAR(50) NOT NULL,
    type           VARCHAR(50) NOT NULL,
    text           VARCHAR(50),
    audio          VARCHAR(100),
    id_personnel   INT,
    id_pictogramme INT,
    PRIMARY KEY (id_element),
    FOREIGN KEY (id_personnel) REFERENCES EducAdmin (id_personnel),
    FOREIGN KEY (id_pictogramme) REFERENCES Pictogramme (id_pictogramme)
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
    etat_fiche           BOOLEAN,
    date_creation        DATETIME,
    commentaire_text_eleve    TEXT,
    commentaire_audio_eleve    TEXT,
    id_personnel         INT NOT NULL,
    id_apprenti          INT NOT NULL,
    PRIMARY KEY (id_fiche),
    FOREIGN KEY (id_personnel) REFERENCES EducAdmin (id_personnel),
    FOREIGN KEY (id_apprenti) REFERENCES Apprenti (id_apprenti),
    CONSTRAINT ch_fiche_degre CHECK (FicheIntervention.degre_urgence >= 1 AND FicheIntervention.degre_urgence <= 4)
);

CREATE TABLE LaisserTrace
(
    id_personnel      INT,
    horodatage        DATETIME,
    intitule          VARCHAR(50) NOT NULL,
    eval_texte        TEXT NOT NULL,
    commentaire_texte TEXT NOT NULL,
    eval_audio        VARCHAR(255),
    commentaire_audio VARCHAR(50),
    id_fiche          INT NOT NULL,
    PRIMARY KEY (id_personnel, horodatage),
    FOREIGN KEY (id_personnel) REFERENCES Personnel (id_personnel),
    FOREIGN KEY (id_fiche) REFERENCES FicheIntervention (id_fiche)
);

CREATE TABLE Assister
(
    id_apprenti INT,
    id_session  INT,
    PRIMARY KEY (id_apprenti, id_session),
    FOREIGN KEY (id_apprenti) REFERENCES Apprenti (id_apprenti),
    FOREIGN KEY (id_session) REFERENCES Session (id_session)
);

CREATE TABLE ComposerPresentation
(
    id_element         INT,
    id_fiche           INT,
    picto              VARCHAR(50),
    text               VARCHAR(50),
    taille_texte       VARCHAR(50),
    audio              VARCHAR(50),
    police             VARCHAR(50),
    couleur            VARCHAR(50),
    couleur_fond       VARCHAR(50),
    niveau             TINYINT,
    position_elem      VARCHAR(50),
    ordre_saisie_focus VARCHAR(50),
    PRIMARY KEY (id_element, id_fiche),
    FOREIGN KEY (id_element) REFERENCES ElementDefaut (id_element),
    FOREIGN KEY (id_fiche) REFERENCES FicheIntervention (id_fiche)
);



INSERT INTO Apprenti (nom, prenom, mdp, login, photo)
VALUES ('dummy', 'dummy', 'dummy', 'dummy', 'dummy'),
       ('Jacquard', 'Davy',
        '9d1e4686b284d51662885140bb6698c4df76b74120f4ac3321e0873a7024760c9a9b9a153111f4c015817af91aa7d071eb66eb003233e59d108d5d876b83f2b3',
        'DAJ12', 'photo_profile/chanteur.png'),
       ('Guilbert', 'Ange',
        '1cd2acb238967581ee76d7505ab6c7dd88a743069a8f3d246d2ea4a2568e8506842b5316a61f191faae7fa1132f329b1e36f06947a9e7584e05d4411e884daa3',
        'ANG12', 'photo_profile/chirurgien.png'),
       ('Poussin', 'Christian',
        'b4b925b7d4ff1c3635db8f866900ecd331466d03c8d4652e3f79b1246ebbd176d64dba022075bd261033c1e8bceb052afed0c1be78bea36f2d9e46c5dbde645d',
        'CHP14', 'photo_profile/hippie.png'),
       ('Trouvé', 'Éloi',
        'b6d2385e4e07960fed0536d888e38ddb2ddb435e5c714cc065ee809f30b29bcfe1414997ed9467b97a5691afc947a20031b11362ed9ca18d06b90c73d77ad8dd',
        'ELT10', 'photo_profile/marin.png'),
       ('Cordonnier', 'Danny',
        '2b4428f21d701980a10e295871e8a2c7297272b5ec29c29672f05a18e6624e7629a8bba35a6e36457b1dc54daea6879449c13733bc948e827b129329103169dd',
        'DAC15', 'photo_profile/medecin.png'),
       ('Massé', 'Xavier',
        'f2749305122d0f0a305cf1ad6f1f1110ee899c72661dea86ace3c0b215abf9f2c963a2325129f5163aa5e9a04f0eb2662b4b4ec921e8d747ebe3e0d007b2f7b7',
        'XAM11', 'photo_profile/pilote.png'),
       ('Meissa', 'Abdelkhader',
        '406a7ce132f622af2dc675e178fd5121729380183111f1b1d585b4e7937ae60de6f3d76c691ef71adb15ee32fd58d4379c2c3924e29715a3b6c2def9840df3aa',
        'ABM17', 'photo_profile/plongueur.png');

INSERT INTO Personnel (nom, prenom, login, mdp, role)
VALUES ('Dupont', 'Jean', 'JED10',
        'd044ba79445b0cb09cf67529817f8cfc5ff6fa651ea83e4464d83b1135e93f1d6e03ca1adb8e780ad0325840da21cf66047bce904882c75a3b1873b15baede42',
        'SuperAdministrateur'),
       ('Lamar', 'Allain', 'ALL11',
        '1ce50cf1c0c3f55c946489aba6f878b62004a2846756236f16bde59420582fb78c43afcadf056ca59dcda94c2201bd0da9a13c7e6282759f42fa7aa417897f72',
        'Educateur Administrateur'),
       ('DitCharo', 'Mathieu', 'MAD14',
        'a421ce666367afb774b41cbccf0d08fd31d1f7785a355ffa96fd69d7354eecd0b890cfae8f7c838b726dea4558df9f06d5055177c69dc5524d45c63d3a33649b',
        'Educateur Administrateur'),
       ('Oskour', 'Jeanne', 'JEO12',
        'df7b278456c003766887e042c3264dcdef24b1ea7dac8944039c22445062762bc8db57636e4f1fc37dabddd69e64487ee1f2e8e9b8ab621503c6008ff118ca89',
        'Educateur'),
       ('Curry', 'Marie', 'MAC10',
        '86c76f9b58836f546e3c1d6a81cc06ba8cba1167714ebc257302a65c2dc7630732be3c91d3ab8230186df077d782080052e48a68ae0a1e659c7ff46b08889e2a',
        'Educateur'),
       ('Barre', 'Lenny', 'LEB08',
        'd825d45a695b82828f9925960a2300c393146df1d65cc54d45b2fa094ebce4c35a9dc7decda4ee5ed4f281506d4ec1f1e13676cefeaf24a6be6dbaf6a8ba994d',
        'Educateur'),
       ('Zirot', 'Benoit', 'BEZ11',
        '0e3fd69106a65064a44d40c9ea4dcf3117ef3e94b033a2c280dd124c9042af56379f15bc7e8ab67031409694f01cca5e5bd5f0a19b133da5a027e0cd57b1ab88',
        'Educateur'),
       ('Rouselle', 'Fabienne', 'FAR16',
        '783dfa2a9aae67aa236a5bb7644c982d5f41ec2939b478ec400a73b1c071a0d59171c0703edede13d800cd4ea39bfc0f22e583a13312f7af16b6f4d8d94f054a',
        'CIP');

INSERT INTO EducAdmin (id_personnel)
VALUES (2),
       (3);

INSERT INTO Formation (intitule, niveau_qualif, groupe, image)
VALUES ('Parcours plomberie', 3, 1, 'formation_image/plomberie.jpg'),
       ('Parcours maintenance batiment', 3, 2, 'formation_image/maintenance_batiment.jpg');

INSERT INTO Session (theme, cours, duree, id_formation)
VALUES ('Probleme tuyauterie', 'Colmater fuite', 3, 1),
       ('Probleme tuyauterie', 'Remplacer tuyau rouillé', 4, 1),
       ('Probleme tuyauterie', 'Remplacer Joint', 2, 1),
       ('Changement Local', 'Demontage cuvette', 5, 1),
       ('Serrurier', 'Forcer serrure', 6, 2),
       ('Serrurier', 'Demonter serrure', 3, 2),
       ('Electrique', 'Remplacer tube néon', 3, 2);

INSERT INTO Assister (id_apprenti, id_session)
VALUES (2, 1),
       (3, 1),
       (4, 1),
       (5, 1),
       (6, 2),
       (7, 2),
       (8, 2);

INSERT INTO ElementDefaut (libelle, type, text, audio, id_personnel, id_pictogramme)
VALUES ('Intervenant', 'categorie', NULL, NULL, 2, NULL),
       ('Nom de l\'intervenant', 'text-short', NULL, NULL, 2, NULL),
       ('Prénom de l\'intervenant', 'text-short', NULL, NULL, 3, NULL),
       ('Intervention', 'categorie', NULL, NULL, 3, NULL),
       ('Durée de l\'intervention', 'date', NULL, NULL, 3, NULL),
       ('Durée de l\'opération', 'select-time', NULL, NULL, 2, NULL),
       ('Confirmation des informations', 'check', NULL, NULL, 2, NULL),
       ('Type de Maintenance', 'categorie', NULL, NULL, 3, NULL),
       ('améliorative', 'radio', NULL, NULL, 3, NULL),
       ('préventive', 'radio', NULL, NULL, 2, NULL),
       ('corrective', 'radio', NULL, NULL, 2, NULL),
       ('Nature de l\'intervention', 'categorie', NULL, NULL, 3, NULL),
       ('Aménagement', 'radio', NULL, NULL, 3, NULL),
       ('Finitions', 'radio', NULL, NULL, 3, NULL),
       ('Installation sanitaire', 'radio', NULL, NULL, 3, NULL),
       ('Installation électrique', 'radio', NULL, NULL, 3, NULL),
       ('Description du travail', 'categorie', NULL, NULL, 2, NULL),
       ('Travaux réalisés', 'text-area', NULL, NULL, 2, NULL),
       ('Travaux non réalisé', 'text-area', NULL, NULL, 2, NULL),
       ('Nécessite une nouvelle intervention', 'check', NULL, NULL, 2, NULL),
       ('Matériaux utilisés', 'categorie', NULL, NULL, 2, NULL),
       ('Materiel 1', 'select-materiel', NULL, NULL, 2, NULL),
       ('Materiel 2', 'select-materiel', NULL, NULL, 2, NULL),
       ('Materiel 3', 'select-materiel', NULL, NULL, 2, NULL),
       ('Materiel 4', 'select-materiel', NULL, NULL, 3, NULL),
       ('Materiel 5', 'select-materiel', NULL, NULL, 3, NULL),
       ('Materiel 6', 'select-materiel', NULL, NULL, 3, NULL),
       ('Materiel 7', 'select-materiel', NULL, NULL, 3, NULL),
       ('Materiel 8', 'select-materiel', NULL, NULL, 3, NULL),
       ('Materiel 9', 'select-materiel', NULL, NULL, 3, NULL),
       ('Materiel 10', 'select-materiel', NULL, NULL, 3, NULL);

INSERT INTO FicheIntervention (id_fiche, numero, nom_du_demandeur, date_demande, localisation, description_demande,
                               degre_urgence, couleur_intervention, etat_fiche, date_creation, commentaire_text_eleve,
                               commentaire_audio_eleve, id_personnel, id_apprenti)
VALUES (1, 0, 'dummy', '1990-01-01', 'dummy', 'dummy', 4, 'vert', 0, '1999-01-01 01:01:01', 'dummy', NUll, 2, 1),
       (2, 1, 'Mermaid Corp', '2023-11-03', 'Espace Lingerie', 'Lorem Ipsum 1', 3, 'jaune', 0, '2023-11-03 12:30:00',
        'Dur dur', NUll, 2, 2),
       (3, 1, 'CROUS', '2023-11-05', 'Batiment A', 'Lorem Ipsum 2', 2, 'orange', 1, '2023-10-05 07:12:01',
        'Ca vas', NUll, 2, 3),
       (4, 1, 'La Region', '2023-05-08', 'Ecole ST Maurice', 'Lorem Ipsum 3', 1, 'rouge', 1, '2023-05-08 14:34:01',
        'Un peu de mal', NUll, 3, 4),
       (5, 1, 'Epicier', '2023-05-26', 'Arriere boutique', 'Lorem Ipsum 4', 3, 'jaune', 0, '2023-05-24 01:01:01',
        'Commentaire', NUll, 3, 5);


INSERT INTO ComposerPresentation (id_element, id_fiche, picto, text, taille_texte, audio, police, couleur, couleur_fond,
                                  niveau, position_elem, ordre_saisie_focus)
VALUES (1, 1, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '10', NULL),
       (2, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '11', NULL),
       (3, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '12', NULL),
       (4, 1, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '20', NULL),
       (5, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '21', NULL),
       (6, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '22', NULL),
       (7, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '23', NULL),
       (8, 1, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '30', NULL),
       (9, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '31', NULL),
       (10, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '32', NULL),
       (11, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '33', NULL),
       (12, 1, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '40', NULL),
       (13, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '41', NULL),
       (14, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '42', NULL),
       (15, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '43', NULL),
       (16, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '44', NULL),
       (17, 1, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '50', NULL),
       (18, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '51', NULL),
       (19, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '52', NULL),
       (20, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '53', NULL),
       (21, 1, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '60', NULL),
       (22, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '61', NULL),
       (23, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '62', NULL),
       (24, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '63', NULL),
       (25, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '64', NULL),
       (26, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '65', NULL),
       (27, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '66', NULL),
       (28, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '67', NULL),
       (29, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '68', NULL),
       (30, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '69', NULL),
       (31, 1, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '610', NULL),
       (1, 2, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '10', NULL),
       (2, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '11', NULL),
       (3, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '12', NULL),
       (4, 2, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '20', NULL),
       (5, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '21', NULL),
       (6, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '22', NULL),
       (7, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '23', NULL),
       (8, 2, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '30', NULL),
       (9, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '31', NULL),
       (10, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '32', NULL),
       (11, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '33', NULL),
       (12, 2, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '40', NULL),
       (13, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '41', NULL),
       (14, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '42', NULL),
       (15, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '43', NULL),
       (16, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '44', NULL),
       (17, 2, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '50', NULL),
       (18, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '51', NULL),
       (19, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '52', NULL),
       (20, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '53', NULL),
       (21, 2, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '60', NULL),
       (22, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '61', NULL),
       (23, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '62', NULL),
       (24, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '63', NULL),
       (25, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '64', NULL),
       (26, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '65', NULL),
       (27, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '66', NULL),
       (28, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '67', NULL),
       (29, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '68', NULL),
       (30, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '69', NULL),
       (31, 2, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '610', NULL),
       (1, 3, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '10', NULL),
       (2, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '11', NULL),
       (3, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '12', NULL),
       (4, 3, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '20', NULL),
       (5, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '21', NULL),
       (6, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '22', NULL),
       (7, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '23', NULL),
       (8, 3, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '30', NULL),
       (9, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '31', NULL),
       (10, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '32', NULL),
       (11, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '33', NULL),
       (12, 3, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '40', NULL),
       (13, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '41', NULL),
       (14, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '42', NULL),
       (15, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '43', NULL),
       (16, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '44', NULL),
       (17, 3, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '50', NULL),
       (18, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '51', NULL),
       (19, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '52', NULL),
       (20, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '53', NULL),
       (21, 3, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '60', NULL),
       (22, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '61', NULL),
       (23, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '62', NULL),
       (24, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '63', NULL),
       (25, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '64', NULL),
       (26, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '65', NULL),
       (27, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '66', NULL),
       (28, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '67', NULL),
       (29, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '68', NULL),
       (30, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '69', NULL),
       (31, 3, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '610', NULL),
       (1, 4, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '10', NULL),
       (2, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '11', NULL),
       (3, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '12', NULL),
       (4, 4, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '20', NULL),
       (5, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '21', NULL),
       (6, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '22', NULL),
       (7, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '23', NULL),
       (8, 4, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '30', NULL),
       (9, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '31', NULL),
       (10, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '32', NULL),
       (11, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '33', NULL),
       (12, 4, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '40', NULL),
       (13, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '41', NULL),
       (14, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '42', NULL),
       (15, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '43', NULL),
       (16, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '44', NULL),
       (17, 4, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '50', NULL),
       (18, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '51', NULL),
       (19, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '52', NULL),
       (20, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '53', NULL),
       (21, 4, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '60', NULL),
       (22, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '61', NULL),
       (23, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '62', NULL),
       (24, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '63', NULL),
       (25, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '64', NULL),
       (26, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '65', NULL),
       (27, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '66', NULL),
       (28, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '67', NULL),
       (29, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '68', NULL),
       (30, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '69', NULL),
       (31, 4, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '610', NULL),
       (1, 5, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '10', NULL),
       (2, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '11', NULL),
       (3, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '12', NULL),
       (4, 5, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '20', NULL),
       (5, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '21', NULL),
       (6, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '22', NULL),
       (7, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '23', NULL),
       (8, 5, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '30', NULL),
       (9, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '31', NULL),
       (10, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '32', NULL),
       (11, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '33', NULL),
       (12, 5, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '40', NULL),
       (13, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '41', NULL),
       (14, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '42', NULL),
       (15, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '43', NULL),
       (16, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '44', NULL),
       (17, 5, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '50', NULL),
       (18, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '51', NULL),
       (19, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '52', NULL),
       (20, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '53', NULL),
       (21, 5, NULL, NULL, 15, NULL, 'Oswald', 'black', NULL, NULL, '60', NULL),
       (22, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '61', NULL),
       (23, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '62', NULL),
       (24, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '63', NULL),
       (25, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '64', NULL),
       (26, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '65', NULL),
       (27, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '66', NULL),
       (28, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '67', NULL),
       (29, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '68', NULL),
       (30, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '69', NULL),
       (31, 5, NULL, NULL, 15, NULL, 'Montserrat', 'black', 'white', 1, '610', NULL);