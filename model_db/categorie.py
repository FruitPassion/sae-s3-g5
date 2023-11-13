from model_db.shared_model import db


class Categorie(db.Model):
    __tablename__ = 'Categorie'
    __table_args__ = {'schema': 'db_fiches_dev'}

    id_categorie = db.Columndb.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(50), nullable=False)
    id_fiche = db.Column(db.ForeignKey(f'db_fiches_dev.FicheIntervention.id_fiche'), nullable=False, index=True)

    FicheIntervention = db.relationship('FicheIntervention', primaryjoin='Categorie.id_fiche == '
                                                                         'FicheIntervention.id_fiche',
                                        backref='categories')
