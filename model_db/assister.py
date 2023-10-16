from model_db.shared_model import db


class Assister(db.Model):
    __tablename__ = 'Assister'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_apprenti = db.Column(db.ForeignKey(f'db_fiches_dev.Apprenti.id_apprenti'), primary_key=True)
    id_session = db.Column(db.ForeignKey(f'db_fiches_dev.Session.id_session'), primary_key=True)

    Apprenti = db.relationship('Apprenti', primaryjoin='Assister.id_apprenti == Apprenti.id_apprenti',
                                backref='assistes')
    Session = db.relationship('Session', primaryjoin='Assister.id_session == Session.id_session',
                               backref='assistes')
