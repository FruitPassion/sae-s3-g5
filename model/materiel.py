from custom_paquets.gestions_erreur import suplement_erreur
from model.shared_model import DB_SCHEMA, db


class Materiel(db.Model):
    __tablename__ = "Materiel"
    __table_args__ = {"schema": DB_SCHEMA}

    id_materiel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    lien = db.Column(db.String(100), nullable=False)

    @staticmethod
    def get_all_materiel():
        """
        Récupère tout le matériel

        :return: liste de tous les matériels
        """
        return Materiel.query.all()

    @staticmethod
    def add_materiel(nom, categorie, lien, commit=True):
        """
        Ajoute un matériel en BD

        """
        try:
            materiel = Materiel(nom=nom, categorie=categorie, lien=lien)
            db.session.add(materiel)
            if commit:
                db.session.commit()

        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de l'ajout du matériel {nom} dans la catégorie {categorie}")

    @staticmethod
    def update_materiel(identifiant, nom, categorie, lien, commit=True):
        """
        Modifie un matériel en BD

        """
        try:
            materiel = Materiel.query.filter_by(id_materiel=identifiant).first()
            materiel.nom = nom
            materiel.categorie = categorie
            materiel.lien = lien
            if commit:
                db.session.commit()

        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la modification du matériel {nom}")

    @staticmethod
    def get_photo_materiel(id_materiel):
        try:
            return Materiel.query.filter_by(id_materiel=id_materiel).with_entities(Materiel.lien).first().lien
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la récupération du lien de la photo du matériel {id_materiel}.")

    @staticmethod
    def remove_materiel(id_materiel, commit=True):
        """
        Supprime un materiel en BD

        :param id_materiel: id de la materiel à supprimer
        :return: None
        """
        try:
            db.session.delete(Materiel.query.filter_by(id_materiel=id_materiel).first())
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la suppression du matériel {id_materiel}.")
            return False

    @staticmethod
    def get_all_categories_materiel():
        """
        Récupère toutes les catégories du matériel

        """
        try:
            return Materiel.query.with_entities(Materiel.categorie).distinct().all()
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la récupération des catégories du matériel")
