from model_db.shared_model import db


class EducAdmin(db.Model):
    __tablename__ = 'EducAdmin'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_personnel = db.Column(db.ForeignKey('db_fiches_dev.Personnel.id_personnel'), primary_key=True)

    Personnel = db.relationship('Personnel', primaryjoin='EducAdmin.id_personnel == Personnel.id_personnel',
                                backref='educadmins')

