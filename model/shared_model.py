from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

FICHE_PERSONNEL = 'db_fiches_dev.Personnel.id_personnel'


class Apprenti(db.Model):
    __tablename__ = 'Apprenti'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_apprenti = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    mdp = db.Column(db.Text)
    photo = db.Column(db.String(100))
    essais = db.Column(db.Integer, nullable=False, default=0)
    archive = db.Column(db.Boolean, nullable=False, default=False)
    adaptation_situation_examen = db.Column(db.Text)


class Assister(db.Model):
    __tablename__ = 'Assister'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_apprenti = db.Column(db.ForeignKey('db_fiches_dev.Apprenti.id_apprenti'), primary_key=True)
    id_cours = db.Column(db.ForeignKey('db_fiches_dev.Cours.id_cours'), primary_key=True)

    Apprenti = db.relationship('Apprenti', primaryjoin='Assister.id_apprenti == Apprenti.id_apprenti',
                               backref='assistes')
    Cours = db.relationship('Cours', primaryjoin='Assister.id_cours == Cours.id_cours',
                            backref='assistes')


class Materiel(db.Model):
    __tablename__ = 'Materiel'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_materiel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    lien = db.Column(db.String(100), nullable=False)


class ComposerPresentation(db.Model):
    __tablename__ = 'ComposerPresentation'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_element = db.Column(db.ForeignKey('db_fiches_dev.ElementBase.id_element'), primary_key=True)
    id_fiche = db.Column(db.ForeignKey('db_fiches_dev.FicheIntervention.id_fiche'), primary_key=True)
    text = db.Column(db.String(50))
    taille_texte = db.Column(db.String(50))
    audio = db.Column(db.String(50))
    police = db.Column(db.String(50))
    couleur = db.Column(db.String(7))
    couleur_fond = db.Column(db.String(7))
    niveau = db.Column(db.Integer)
    position_elem = db.Column(db.String(50))
    ordre_saisie_focus = db.Column(db.String(50))
    id_pictogramme = db.Column(db.ForeignKey('db_fiches_dev.Pictogramme.id_pictogramme'), index=True)
    taille_pictogramme = db.Column(db.Integer)
    couleur_pictogramme = db.Column(db.String(7))
    id_materiel = db.Column(db.ForeignKey('db_fiches_dev.Materiel.id_materiel'), index=True)

    ElementBase = db.relationship('ElementBase',
                                  primaryjoin='ComposerPresentation.id_element == ElementBase.id_element',
                                  backref='composerpresentations')
    FicheIntervention = db.relationship('FicheIntervention',
                                        primaryjoin='ComposerPresentation.id_fiche == FicheIntervention.id_fiche',
                                        backref='composerpresentations')
    Pictogramme = db.relationship('Pictogramme',
                                  primaryjoin='ComposerPresentation.id_pictogramme == Pictogramme.id_pictogramme',
                                  backref='composerpresentations')


class EducAdmin(db.Model):
    __tablename__ = 'EducAdmin'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_personnel = db.Column(db.ForeignKey(FICHE_PERSONNEL), primary_key=True)

    Personnel = db.relationship('Personnel', primaryjoin='EducAdmin.id_personnel == Personnel.id_personnel',
                                backref='educadmins')


class ElementBase(db.Model):
    __tablename__ = 'ElementBase'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_element = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(50))
    audio = db.Column(db.String(100))


class FicheIntervention(db.Model):
    __tablename__ = 'FicheIntervention'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_fiche = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Integer, nullable=False)
    nom_du_demandeur = db.Column(db.String(50))
    date_demande = db.Column(db.Date)
    localisation = db.Column(db.String(50))
    description_demande = db.Column(db.Text)
    degre_urgence = db.Column(db.Integer)
    couleur_intervention = db.Column(db.String(50))
    etat_fiche = db.Column(db.Integer)
    date_creation = db.Column(db.DateTime)
    photo_avant = db.Column(db.String(150))
    photo_apres = db.Column(db.String(150))
    nom_intervenant = db.Column(db.String(50), nullable=False)
    prenom_intervenant = db.Column(db.String(50), nullable=False)
    id_apprenti = db.Column(db.ForeignKey('db_fiches_dev.Apprenti.id_apprenti'), nullable=False, index=True)
    id_personnel = db.Column(db.ForeignKey(FICHE_PERSONNEL), nullable=False, index=True)
    id_cours = db.Column(db.ForeignKey('db_fiches_dev.Cours.id_cours'), nullable=False, index=True)

    Apprenti = db.relationship('Apprenti', primaryjoin='FicheIntervention.id_apprenti == Apprenti.id_apprenti',
                               backref='fiches')
    Personnel = db.relationship('Personnel', primaryjoin='FicheIntervention.id_personnel == Personnel.id_personnel',
                                backref='fiches')
    Cours = db.relationship('Cours', primaryjoin='FicheIntervention.id_cours == Cours.id_cours',
                            backref='fiches')


class Formation(db.Model):
    __tablename__ = 'Formation'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_formation = db.Column(db.Integer, primary_key=True, autoincrement=True)
    intitule = db.Column(db.String(50), nullable=False)
    niveau_qualif = db.Column(db.Integer)
    groupe = db.Column(db.String(50))
    image = db.Column(db.String(100))
    archive = db.Column(db.Boolean, nullable=False, default=False)


class LaisserTrace(db.Model):
    __tablename__ = 'LaisserTrace'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_personnel = db.Column(db.ForeignKey(FICHE_PERSONNEL), primary_key=True)
    horodatage = db.Column(db.DateTime, primary_key=True)
    intitule = db.Column(db.String(50), nullable=False)
    eval_texte = db.Column(db.Text, nullable=False)
    commentaire_texte = db.Column(db.Text, nullable=False)
    eval_audio = db.Column(db.String(255))
    commentaire_audio = db.Column(db.String(50))
    apprenti = db.Column(db.Integer, nullable=True)
    id_fiche = db.Column(db.ForeignKey('db_fiches_dev.FicheIntervention.id_fiche'), nullable=False, index=True)

    FicheIntervention = db.relationship('FicheIntervention',
                                        primaryjoin='LaisserTrace.id_fiche == FicheIntervention.id_fiche',
                                        backref='traces')
    Personnel = db.relationship('Personnel', primaryjoin='LaisserTrace.id_personnel == Personnel.id_personnel',
                                backref='traces')


class Personnel(db.Model):
    __tablename__ = 'Personnel'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_personnel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    mdp = db.Column(db.Text)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    essais = db.Column(db.Integer, nullable=False, default=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)


class Pictogramme(db.Model):
    __tablename__ = 'Pictogramme'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_pictogramme = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    souscategorie = db.Column(db.String(50), nullable=False)


class Cours(db.Model):
    __tablename__ = 'Cours'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_cours = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(50), nullable=False)
    cours = db.Column(db.String(50), nullable=False)
    duree = db.Column(db.Integer)
    archive = db.Column(db.Boolean, nullable=False, default=False)
    id_formation = db.Column(db.ForeignKey('db_fiches_dev.Formation.id_formation'), nullable=False, index=True)

    Formation = db.relationship('Formation', primaryjoin='Cours.id_formation == Formation.id_formation',
                                backref='cours')
