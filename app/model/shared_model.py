from flask_sqlalchemy import SQLAlchemy

from custom_paquets.app_checker import lire_config

db = SQLAlchemy()

config = lire_config("config.txt")

if config == "test":
    DB_SCHEMA = "main"
else:
    DB_SCHEMA = f"db_fiches_{config.lower()}"


class Assister(db.Model):
    __tablename__ = "Assister"
    __table_args__ = {"schema": DB_SCHEMA}

    id_apprenti = db.Column(db.ForeignKey(f"{DB_SCHEMA}.Apprenti.id_apprenti"), primary_key=True)
    id_cours = db.Column(db.ForeignKey(f"{DB_SCHEMA}.Cours.id_cours"), primary_key=True)

    Apprenti = db.relationship("Apprenti", primaryjoin="Assister.id_apprenti == Apprenti.id_apprenti", backref="assistes")
    Cours = db.relationship("Cours", primaryjoin="Assister.id_cours == Cours.id_cours", backref="assistes")


class EducAdmin(db.Model):
    __tablename__ = "EducAdmin"
    __table_args__ = {"schema": DB_SCHEMA}

    id_personnel = db.Column(db.ForeignKey(f"{DB_SCHEMA}.Personnel.id_personnel"), primary_key=True)

    Personnel = db.relationship("Personnel", primaryjoin="EducAdmin.id_personnel == Personnel.id_personnel", backref="educadmins")


class ElementBase(db.Model):
    __tablename__ = "ElementBase"
    __table_args__ = {"schema": DB_SCHEMA}

    id_element = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(50))
    audio = db.Column(db.String(100))
