from model_db.shared_model import db


class Session(db.Model):
    __tablename__ = 'Session'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_session = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(50), nullable=False)
    cours = db.Column(db.String(50), nullable=False)
    Debut = db.Column(db.Date, nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    id_formation = db.Column(db.ForeignKey(f'db_fiches_dev.Formation.id_formation'), nullable=False, index=True)

    Formation = db.relationship('Formation', primaryjoin='Session.id_formation == Formation.id_formation',
                                backref='sessions')
