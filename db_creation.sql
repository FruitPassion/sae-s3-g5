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
   mdp TEXT NOT NULL,
   role VARCHAR(50),
   PRIMARY KEY(id_personnel)
);

CREATE TABLE Apprenti(
   id_apprenti INT AUTO_INCREMENT,
   nom VARCHAR(50) NOT NULL,
   prenom VARCHAR(50) NOT NULL,
   login VARCHAR(50),
   mdp TEXT,
   photo VARCHAR(50),
   PRIMARY KEY(id_apprenti)
);

CREATE TABLE Formation(
   id_formation INT AUTO_INCREMENT,
   intitule VARCHAR(50) NOT NULL,
   niveau_qualif SMALLINT,
   groupe VARCHAR(50),
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
   Id_Pictogramme INT AUTO_INCREMENT,
   label VARCHAR(50),
   url VARCHAR(100),
   categorie VARCHAR(50),
   PRIMARY KEY(Id_Pictogramme)
);

CREATE TABLE FicheIntervention(
   id_fiche INT AUTO_INCREMENT,
   numero SMALLINT,
   nom_demandeur VARCHAR(50),
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
   FOREIGN KEY(id_personnel) REFERENCES EducAdmin(id_personnel),
   FOREIGN KEY(id_apprenti) REFERENCES Apprenti(id_apprenti)
);

CREATE TABLE Categorie(
   id_categorie INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   id_fiche INT NOT NULL,
   PRIMARY KEY(id_categorie),
   FOREIGN KEY(id_fiche) REFERENCES FicheIntervention(id_fiche)
);

CREATE TABLE ElementDefaut(
   id_element INT AUTO_INCREMENT,
   type VARCHAR(50),
   texte VARCHAR(50),
   audio VARCHAR(50),
   id_categorie INT NOT NULL,
   id_pictogramme INT NOT NULL,
   id_personnel INT NOT NULL,
   PRIMARY KEY(id_element),
   FOREIGN KEY(Id_Categorie) REFERENCES Categorie(id_categorie),
   FOREIGN KEY(id_pictogramme) REFERENCES Pictogramme(id_pictogramme),
   FOREIGN KEY(id_personnel) REFERENCES EducAdmin(id_personnel)
);

CREATE TABLE LaisserTrace(
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
   police VARCHAR(50),
   texte VARCHAR(50),
   niveau TINYINT,
   couleur VARCHAR(50),
   couleur_fond VARCHAR(50),
   audio VARCHAR(50),
   picto VARCHAR(50),
   taille_texte VARCHAR(50),
   PRIMARY KEY(id_element, id_fiche),
   FOREIGN KEY(id_element) REFERENCES ElementDefaut(id_element),
   FOREIGN KEY(id_fiche) REFERENCES FicheIntervention(id_fiche)
);


INSERT INTO Apprenti (nom, prenom, mdp, login)
VALUES ('Jacquard', 'Davy', '9d1e4686b284d51662885140bb6698c4df76b74120f4ac3321e0873a7024760c9a9b9a153111f4c015817af91aa7d071eb66eb003233e59d108d5d876b83f2b3', 'DAJ12'),
       ('Guilbert', 'Ange', '1cd2acb238967581ee76d7505ab6c7dd88a743069a8f3d246d2ea4a2568e8506842b5316a61f191faae7fa1132f329b1e36f06947a9e7584e05d4411e884daa3', 'ANG12'),
       ('Poussin', 'Christian', 'b4b925b7d4ff1c3635db8f866900ecd331466d03c8d4652e3f79b1246ebbd176d64dba022075bd261033c1e8bceb052afed0c1be78bea36f2d9e46c5dbde645d', 'CHP14'),
       ('Trouvé', 'Éloi', 'b6d2385e4e07960fed0536d888e38ddb2ddb435e5c714cc065ee809f30b29bcfe1414997ed9467b97a5691afc947a20031b11362ed9ca18d06b90c73d77ad8dd', 'ELT10'),
       ('Cordonnier', 'Danny', '2b4428f21d701980a10e295871e8a2c7297272b5ec29c29672f05a18e6624e7629a8bba35a6e36457b1dc54daea6879449c13733bc948e827b129329103169dd', 'DAC15'),
       ('Massé', 'Xavier', 'f2749305122d0f0a305cf1ad6f1f1110ee899c72661dea86ace3c0b215abf9f2c963a2325129f5163aa5e9a04f0eb2662b4b4ec921e8d747ebe3e0d007b2f7b7', 'XAM11'),
       ('Meissa', 'Abdelkhader', '406a7ce132f622af2dc675e178fd5121729380183111f1b1d585b4e7937ae60de6f3d76c691ef71adb15ee32fd58d4379c2c3924e29715a3b6c2def9840df3aa', 'ABM17');

INSERT INTO Personnel (nom, prenom, login, mdp, role)
VALUES ('Dupont', 'Jean', 'JED10', 'd044ba79445b0cb09cf67529817f8cfc5ff6fa651ea83e4464d83b1135e93f1d6e03ca1adb8e780ad0325840da21cf66047bce904882c75a3b1873b15baede42','SuperAdministrateur'),
       ('Lamar', 'Allain', 'ALL11', '1ce50cf1c0c3f55c946489aba6f878b62004a2846756236f16bde59420582fb78c43afcadf056ca59dcda94c2201bd0da9a13c7e6282759f42fa7aa417897f72','Educateur Administrateur'),
       ('DitCharo', 'Mathieu', 'MAD14', 'a421ce666367afb774b41cbccf0d08fd31d1f7785a355ffa96fd69d7354eecd0b890cfae8f7c838b726dea4558df9f06d5055177c69dc5524d45c63d3a33649b','Educateur Administrateur'),
       ('Oskour', 'Jeanne', 'JEO12', 'df7b278456c003766887e042c3264dcdef24b1ea7dac8944039c22445062762bc8db57636e4f1fc37dabddd69e64487ee1f2e8e9b8ab621503c6008ff118ca89', 'Educateur'),
       ('Curry', 'Marie', 'MAC10', '86c76f9b58836f546e3c1d6a81cc06ba8cba1167714ebc257302a65c2dc7630732be3c91d3ab8230186df077d782080052e48a68ae0a1e659c7ff46b08889e2a', 'Educateur'),
       ('Barre', 'Lenny', 'LEB08', 'd825d45a695b82828f9925960a2300c393146df1d65cc54d45b2fa094ebce4c35a9dc7decda4ee5ed4f281506d4ec1f1e13676cefeaf24a6be6dbaf6a8ba994d', 'Educateur'),
       ('Zirot', 'Benoit', 'BEZ11', '0e3fd69106a65064a44d40c9ea4dcf3117ef3e94b033a2c280dd124c9042af56379f15bc7e8ab67031409694f01cca5e5bd5f0a19b133da5a027e0cd57b1ab88', 'Educateur'),
       ('Rouselle', 'Fabienne', 'FAR16', '783dfa2a9aae67aa236a5bb7644c982d5f41ec2939b478ec400a73b1c071a0d59171c0703edede13d800cd4ea39bfc0f22e583a13312f7af16b6f4d8d94f054a', 'CIP');

INSERT INTO Formation (intitule, niveau_qualif, groupe)
VALUES ('Parcours plomberie','CAP',1),
       ('Agent de maintenance en bâtiment','Licence',2);

INSERT INTO Assister (id_apprenti, id_formation)
VALUES (1, 1),
       (2, 1),
       (3, 1),
       (4, 1),
       (5, 2),
       (6, 2),
       (7, 2);


