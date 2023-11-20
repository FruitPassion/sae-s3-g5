from model_db.shared_model import db
from model_db.assister import Assister


class Formation(db.Model):
    __tablename__ = 'Formation'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_formation = db.Column(db.Integer, primary_key=True, autoincrement=True)
    intitule = db.Column(db.String(50), nullable=False)
    niveau_qualif = db.Column(db.Integer)
    groupe = db.Column(db.String(50))
    image = db.Column(db.String(100))

