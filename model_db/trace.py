from model_db.shared_model import db


class Trace(db.Model):
    __tablename__ = 'Trace'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_personnel = db.Column(db.ForeignKey('db_fiches_dev.Personnel.id_personnel'), primary_key=True)
    horodatage = db.Column(db.Datetime, primary_key=True)
    intitule = db.Column(db.String(50), nullable=False)
    eval_texte = db.Column(db.Text, nullable=False)
    commentaire_texte = db.Column(db.Text, nullable=False)
    eval_audio = db.Column(db.String(255))
    commentaire_audio = db.Column(db.String(50))
    id_fiche = db.Columndb.Column(db.ForeignKey('db_fiches_dev.Fiche.id_fiche'), nullable=False, index=True)

    Fiche = db.relationship('Fiche', primaryjoin='Trace.id_fiche == Fiche.id_fiche', backref='traces')
    Personnel = db.relationship('Personnel', primaryjoin='Trace.id_personnel == Personnel.id_personnel',
                                backref='traces')

