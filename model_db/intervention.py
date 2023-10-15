from model_db.shared_model import db


class Intervention(db.Model):
    __tablename__ = 'Intervention'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Intervention = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    DateIntervention = db.Column(db.Date, nullable=False)
    TypeIntervention = db.Column(db.String(50), nullable=False)
    NatureIntervention = db.Column(db.String(50), nullable=False)
