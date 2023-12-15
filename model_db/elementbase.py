from model_db.shared_model import db


class ElementBase(db.Model):
    __tablename__ = 'ElementBase'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_element = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(50))
    audio = db.Column(db.String(100))
    id_personnel = db.Column(db.ForeignKey('db_fiches_dev.Personnel.id_personnel'), index=True)

    Personnel = db.relationship('Personnel', primaryjoin='ElementBase.id_personnel == Personnel.id_personnel',
                                backref='elementbases')
