from model_db.shared_model import db


class Avoir(db.Model):
    __tablename__ = 'Avoir'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Fiche = db.Columndb.Column(db.ForeignKey(f'db_fiches_dev.Fiche.Id_Fiche'), primary_key=True)
    Id_ElementForm = db.Column(db.ForeignKey(f'db_fiches_dev.ElementForm.Id_ElementForm'), primary_key=True)

    Fiche = db.relationship('Fiche', primaryjoin='Avoir.Id_Fiche == Fiche.Id_Fiche', backref='avoirs')
    ElementForm = db.relationship('ElementForm', primaryjoin='ElementForm.Id_ElementForm == ElementForm.Id_ElementForm',
                                backref='avoirs')

