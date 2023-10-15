from model_db.shared_model import db


class Trace(db.Model):
    __tablename__ = 'Trace'
    __table_args__ = {'schema': 'db_fiches_dev'}

    DateFinFiche = db.Column(db.Datetime, primary_key=True)
    Id_Fiche = db.Columndb.Column(db.ForeignKey(f'db_fiches_dev.Fiche.Id_Fiche'), primary_key=True)
    Intitule = db.Column(db.String(50), nullable=False)
    EvalTextuelle = db.Column(db.Text, nullable=False)
    EvalAudio = db.Column(db.String(100))
    CommentaireTextuel = db.Column(db.Text, nullable=False)
    CommentaireAudio = db.Column(db.String(100))
    Id_Personnel = db.Column(db.ForeignKey(f'db_fiches_dev.Personnel.Id_Personnel'), nullable=False, index=True)

    Fiche = db.relationship('Fiche', primaryjoin='Trace.Id_Fiche == Fiche.Id_Fiche', backref='traces')
    Personnel = db.relationship('Personnel', primaryjoin='Trace.Id_Personnel == Personnel.Id_Personnel',
                                backref='traces')

