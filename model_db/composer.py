from model_db.shared_model import db


class Composer(db.Model):
    __tablename__ = 'Composer'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_element = db.Column(db.ForeignKey('db_fiches_dev.ElementDefaut.id_element'), primary_key=True)
    id_fiche = db.Column(db.ForeignKey('db_fiches_dev.Fiche.id_fiche'), primary_key=True)
    picto = db.Column(db.String(50))
    text = db.Column(db.String(50))
    taille_texte = db.Column(db.String(50))
    police = db.Column(db.String(50))
    audio = db.Column(db.String(50))
    couleur = db.Column(db.String(50))
    couleur_fond = db.Column(db.String(50))
    niveau = db.Column(db.Integer)

    ElementDefaut = db.relationship('ElementDefaut',
                                    primaryjoin='Composer.id_element == ElementDefaut.id_element',
                                    backref='composers')
    FicheIntervention = db.relationship('FicheIntervention',
                                        primaryjoin='Composer.id_fiche == FicheIntervention.id_fiche',
                                        backref='composers')
