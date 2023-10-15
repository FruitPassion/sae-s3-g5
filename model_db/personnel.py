from model_db.shared_model import db


class Personnel(db.Model):
    __tablename__ = 'Personnel'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Personnel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom = db.Column(db.String(50), nullable=False)
    Prenom = db.Column(db.String(50), nullable=False)
    Login = db.Column(db.String(50), nullable=False)
    MDP = db.Column(db.Text, nullable=False)
    Role = db.Column(db.String(50), nullable=False)
