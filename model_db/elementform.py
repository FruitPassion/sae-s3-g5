from model_db.shared_model import db


class ElementForm(db.Model):
    __tablename__ = 'ElementForm'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_ElementForm = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    TypeElt = db.Column(db.String(50), nullable=False)
    Picto = db.Column(db.String(100))
    Libelle = db.Column(db.String(100), nullable=False)
    Audio = db.Column(db.String(100))
    TailleLibelle = db.Column(db.Integer, nullable=False)
    PoliceLibelle = db.Column(db.String(50), nullable=False)
    CouleurLibelle = db.Column(db.String(6), nullable=False)
    CouleurFondLib = db.Column(db.String(6), nullable=False)
    NiveauAffichage = db.Column(db.Integer, nullable=False)
    DateHeure = db.Column(db.Datetime, nullable=False)
    ReponseApprenti = db.Column(db.Text)

