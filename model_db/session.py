from model_db.shared_model import db


class Session(db.Model):
    __tablename__ = 'Session'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_session = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(50), nullable=False)
    cours = db.Column(db.String(50), nullable=False)
    duree = db.Column(db.Integer)
    id_formation = db.Column(db.ForeignKey('db_fiches_dev.Formation.id_formation'), nullable=False, index=True)

    Formation = db.relationship('Formation', primaryjoin='Session.id_formation == Formation.id_formation',
                                backref='sessions')
