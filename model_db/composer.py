from model_db.shared_model import db


class ComposerPresentation(db.Model):
    __tablename__ = 'ComposerPresentation'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_element = db.Column(db.ForeignKey('db_fiches_dev.ElementBase.id_element'), primary_key=True)
    id_fiche = db.Column(db.ForeignKey('db_fiches_dev.FicheIntervention.id_fiche'), primary_key=True)
    picto = db.Column(db.String(50))
    text = db.Column(db.String(50))
    taille_texte = db.Column(db.String(50))
    audio = db.Column(db.String(50))
    police = db.Column(db.String(50))
    couleur = db.Column(db.String(50))
    couleur_fond = db.Column(db.String(50))
    niveau = db.Column(db.Integer)
    position_elem = db.Column(db.String(50))
    ordre_saisie_focus = db.Column(db.String(50))

    ElementBase = db.relationship('ElementBase',
                                    primaryjoin='ComposerPresentation.id_element == ElementBase.id_element',
                                    backref='composerpresentations')
    FicheIntervention = db.relationship('FicheIntervention',
                                        primaryjoin='ComposerPresentation.id_fiche == FicheIntervention.id_fiche',
                                        backref='composerpresentations')
