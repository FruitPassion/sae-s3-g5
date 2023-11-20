from model_db.shared_model import db


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
    etat_fiche = db.Column(db.Boolean)
    date_creation = db.Column(db.DateTime)
    commentaire_text_eleve = db.Column(db.Text)
    commentaire_audio_eleve = db.Column(db.Text)
    id_apprenti = db.Column(db.ForeignKey('db_fiches_dev.Apprenti.id_apprenti'), nullable=False, index=True)
    id_personnel = db.Column(db.ForeignKey('db_fiches_dev.Personnel.id_personnel'), nullable=False, index=True)

    Apprenti = db.relationship('Apprenti', primaryjoin='FicheIntervention.id_apprenti == Apprenti.id_apprenti',
                               backref='fiches')
    Personnel = db.relationship('Personnel', primaryjoin='FicheIntervention.id_personnel == Personnel.id_personnel',
                                backref='fiches')
