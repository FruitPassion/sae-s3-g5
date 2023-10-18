from model_db.shared_model import db


class Personnel(db.Model):
    __tablename__ = 'Personnel'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_personnel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    mdp = db.Column(db.Text)
    role = db.Column(db.String(50), nullable=False)
