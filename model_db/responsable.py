from model_db.shared_model import db


class Responsable(db.Model):
    __tablename__ = 'Responsable'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Formation = db.Columndb.Column(db.ForeignKey(f'db_fiches_dev.Formation.Id_Formation'), primary_key=True)
    Id_Personnel = db.Column(db.ForeignKey(f'db_fiches_dev.Personnel.Id_Personnel'), primary_key=True)

    Formation = db.relationship('Fiche', primaryjoin='Responsable.Id_Formation == Formation.Id_Formation',
                                backref='responsables')
    Personnel = db.relationship('ElementForm', primaryjoin='Responsable.Id_Personnel == Personnel.Id_Personnel',
                                backref='responsables')

