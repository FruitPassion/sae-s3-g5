from model_db.shared_model import db


class Archiver(db.Model):
    __tablename__ = 'Archiver'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Apprentis = db.Columndb.Column(db.ForeignKey(f'db_fiches_dev.Apprentis.Id_Apprentis'), primary_key=True)
    Date_archive = db.Column(db.Datetime, primary_key=True)
    O_N = db.Column(db.Boolean)
    Id_Personnel = db.Column(db.ForeignKey(f'db_fiches_dev.Personnel.Id_Personnel'), nullable=False, index=True)

    Apprentis = db.relationship('Apprentis', primaryjoin='Archiver.Id_Apprentis == Apprentis.Id_Apprentis',
                                backref='archives')
    Personnel = db.relationship('Personnel', primaryjoin='Archiver.Id_Personnel == Personnel.Id_Personnel',
                                backref='archives')

