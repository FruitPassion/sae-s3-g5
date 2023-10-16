from model_db.shared_model import db


class ElementDefaut(db.Model):
    __tablename__ = 'ElementDefaut'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_element = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
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
    id_pictogramme = db.Column(db.ForeignKey(f'db_fiches_dev.Personnel.Id_Personnel'), primary_key=True)
    id_personnel = db.Column(db.ForeignKey(f'db_fiches_dev.Personnel.Id_Personnel'), primary_key=True)

    Pictogramme = db.relationship('Pictogramme', primaryjoin='ElementDefaut.id_pictogramme == Personnel.Id_Personnel',
                                backref='educadmins')
    Personnel = db.relationship('Personnel', primaryjoin='ElementDefaut.id_personnel == Personnel.Id_Personnel',
                                backref='educadmins')

