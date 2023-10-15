from model_db.shared_model import db


class Session(db.Model):
    __tablename__ = 'Session'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Session = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    Theme = db.Column(db.String(25), nullable=False)
    Cours = db.Column(db.String(50), nullable=False)
    Debut = db.Column(db.Date, nullable=False)
    Duree = db.Column(db.Date, nullable=False)
