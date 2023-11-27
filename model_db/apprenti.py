from model_db.shared_model import db


class Apprenti(db.Model):
    __tablename__ = 'Apprenti'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_apprenti = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    mdp = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(100))
    essaies = db.Column(db.Integer, nullable=False)
