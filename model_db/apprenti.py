from model_db.shared_model import db


class Apprenti(db.Model):
    __tablename__ = 'Commentaire'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Apprenti = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom = db.Column(db.String(50), nullable=False)
    Prenom = db.Column(db.String(50), nullable=False)
    Login = db.Column(db.String(50), nullable=False)
    MDP = db.Column(db.Integer(9), nullable=False)
    Id_Formation = db.Column(db.ForeignKey(f'db_fiches_dev.Formation.Id_Formation'), nullable=False, index=True)

    Formation = db.relationship('Formation', primaryjoin='Apprenti.Id_Formation == Formation.Id_Formation',
                                backref='apprentis')

