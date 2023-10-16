from model_db.shared_model import db


class Formation(db.Model):
    __tablename__ = 'Formation'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_formation = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    intitule = db.Column(db.String(50), nullable=False)
    niveau_qualif = db.Column(db.String(25))
    groupe = db.Column(db.String(50))

