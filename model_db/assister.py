from model_db.shared_model import db


class Assister(db.Model):
    __tablename__ = 'Assister'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_apprenti = db.Column(db.ForeignKey(f'db_fiches_dev.Apprenti.id_apprenti'), primary_key=True)
    id_formation = db.Column(db.ForeignKey(f'db_fiches_dev.Formation.id_formation'), primary_key=True)

    Apprenti = db.relationship('Apprenti', primaryjoin='Assister.id_apprenti == Apprenti.id_apprenti',
                               backref='assistes')
    Formation = db.relationship('Formation', primaryjoin='Assister.id_formation == Formation.id_formation',
                                backref='assistes')
