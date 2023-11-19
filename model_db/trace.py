from model_db.shared_model import db


class Trace(db.Model):
    __tablename__ = 'Trace'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_personnel = db.Column(db.ForeignKey('db_fiches_dev.Personnel.id_personnel'), primary_key=True)
    horodatage = db.Column(db.DateTime, primary_key=True)
    intitule = db.Column(db.String(50), nullable=False)
    eval_texte = db.Column(db.Text, nullable=False)
    commentaire_texte = db.Column(db.Text, nullable=False)
    eval_audio = db.Column(db.String(255))
    commentaire_audio = db.Column(db.String(50))
    id_fiche = db.Column(db.ForeignKey('db_fiches_dev.FicheIntervention.id_fiche'), nullable=False, index=True)

    FicheIntervention = db.relationship('FicheIntervention', primaryjoin='Trace.id_fiche == FicheIntervention.id_fiche', backref='traces')
    Personnel = db.relationship('Personnel', primaryjoin='Trace.id_personnel == Personnel.id_personnel',
                                backref='traces')

