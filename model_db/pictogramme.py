from model_db.shared_model import db


class Pictogramme(db.Model):
    __tablename__ = 'Pictogramme'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_pictogramme = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
