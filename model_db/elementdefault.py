from model_db.shared_model import db


class ElementDefaut(db.Model):
    __tablename__ = 'ElementDefaut'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_element = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(50))
    audio = db.Column(db.String(100))
    id_pictogramme = db.Column(db.ForeignKey('db_fiches_dev.Pictogramme.id_pictogramme'), index=True)
    id_personnel = db.Column(db.ForeignKey('db_fiches_dev.Personnel.id_personnel'), index=True)

    Pictogramme = db.relationship('Pictogramme',
                                  primaryjoin='ElementDefaut.id_pictogramme == Pictogramme.id_pictogramme',
                                  backref='elementdefauts')
    Personnel = db.relationship('Personnel', primaryjoin='ElementDefaut.id_personnel == Personnel.id_personnel',
                                backref='elementdefauts')
