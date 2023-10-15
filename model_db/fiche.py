from model_db.shared_model import db


class Fiche(db.Model):
    __tablename__ = 'Fiche'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Fiche = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    NumFiche = db.Column(db.Integer, nullable=False)
    NomDemandeur = db.Column(db.String(50), nullable=False)
    DateDemande = db.Column(db.Date, nullable=False)
    Localisation = db.Column(db.String(100), nullable=False)
    Descrition = db.Column(db.Text, nullable=False)
    DegreUrgence = db.Column(db.Integer, nullable=False)
    EtatFicheApprenti = db.Column(db.String(50), nullable=False)
    Id_Apprenti = db.Columndb.Column(db.ForeignKey(f'db_fiches_dev.Apprenti.Id_Apprenti'), nullable=False, index=True)
    Id_Intervention = db.Column(db.ForeignKey(f'db_fiches_dev.Intervention.Id_Intervention'), nullable=False,
                                index=True)
    Id_Session = db.Column(db.ForeignKey(f'db_fiches_dev.Session.Id_Session'), nullable=False, index=True)

    Apprenti = db.relationship('Apprenti', primaryjoin='Fiche.Id_Apprenti == Apprenti.Id_Apprenti', backref='fiches')
    Intervention = db.relationship('Intervention', primaryjoin='Fiche.Id_Intervention == Intervention.Id_Intervention',
                                   backref='fiches')
    Session = db.relationship('Session', primaryjoin='Fiche.Id_Session == Session.Id_Session', backref='fiches')

