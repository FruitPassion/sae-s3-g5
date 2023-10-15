from model_db.shared_model import db


class Formation(db.Model):
    __tablename__ = 'Formation'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Formation = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    Intitule = db.Column(db.String(100), nullable=False)
    NiveauQualif = db.Column(db.String(25), nullable=False)

