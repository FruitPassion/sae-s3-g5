from model_db.shared_model import db


class ElementDefaut(db.Model):
    __tablename__ = 'ElementDefaut'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_element = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text)
    audio = db.Column(db.String(100), nullable=False)
    id_pictogramme = db.Column(db.ForeignKey(f'db_fiches_dev.Pictogramme.id_pictogramme'), nullable=False, index=True)
    id_personnel = db.Column(db.ForeignKey(f'db_fiches_dev.Personnel.id_personnel'), nullable=False, index=True)

    Pictogramme = db.relationship('Pictogramme',
                                  primaryjoin='ElementDefaut.id_pictogramme == Pictogramme.id_pictogramme',
                                  backref='elementdefauts')
    Personnel = db.relationship('Personnel', primaryjoin='ElementDefaut.id_personnel == Personnel.id_personnel',
                                backref='elementdefauts')
