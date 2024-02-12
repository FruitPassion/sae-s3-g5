import logging

from model.apprenti import Apprenti
from model.cours import Cours

from model.shared_model import db, DB_SCHEMA, Assister


class Formation(db.Model):
    __tablename__ = 'Formation'
    __table_args__ = {'schema': DB_SCHEMA}

    id_formation = db.Column(db.Integer, primary_key=True, autoincrement=True)
    intitule = db.Column(db.String(50), nullable=False)
    niveau_qualif = db.Column(db.Integer)
    groupe = db.Column(db.String(50))
    image = db.Column(db.String(100))
    archive = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def get_all_formations(archive=False):
        """
        Retourne la liste de toutes les formations

        :param archive: Si True, retourne uniquement les formations archivées
        :return: Une liste de formations
        """
        try:
            return Formation.query.filter(Formation.archive == archive).all()
        except Exception as e:
            logging.error("Erreur lors de la récupération de la liste de toutes les formations")
            logging.error(e)

    @staticmethod
    def get_formation_par_apprenti(login_apprenti):
        """
        Retourne la formation d'un apprenti à partir de son login

        :return: Une formation
        """
        try:
            return Formation.query.with_entities(Formation.intitule).join(Cours).join(Assister).join(Apprenti).filter_by(
                login=login_apprenti).first().intitule
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de la formation de l'apprenti {login_apprenti}")
            logging.error(e)

    @staticmethod
    def get_formation_id_par_nom_formation(nom_formation: str):
        """
        Retourne l'id d'une formation à partir de son nom

        :return: Un id de formation
        """
        try:
            return Formation.query.with_entities(Formation.id_formation).filter_by(
                intitule=nom_formation).first().id_formation
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'id de la formation {nom_formation}")
            logging.error(e)
            return False

    @staticmethod
    def get_nom_formation(id_formation):
        """
        Retourne l'intitulé d'une formation à partir de son id

        :return: Un intitulé de formation
        """
        try:
            return Formation.query.with_entities(Formation.intitule).filter_by(id_formation=id_formation).first().intitule
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du nom de la formation {id_formation}")
            logging.error(e)

    @staticmethod
    def get_image_formation(id_formation):
        try:
            return Formation.query.filter_by(id_formation=id_formation).with_entities(Formation.image).first().image
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'image de la formation {id_formation}")
            logging.error(e)

    @staticmethod
    def add_formation(intitule, niveau_qualif, groupe, image, commit=True):
        """
        Ajoute une formation en BD

        :return: id_formation
        """
        try:
            formation = Formation(intitule=intitule, niveau_qualif=niveau_qualif, groupe=groupe, image=image)
            db.session.add(formation)
            if commit:
                db.session.commit()
            return Formation.get_formation_id_par_nom_formation(intitule)
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout de la formation {intitule}")
            logging.error(e)

    @staticmethod
    def update_formation(identifiant, intitule, niveau_qualif, groupe, image, commit=True):
        """
        Modifie une formation en BD

        :return: None
        """
        try:
            formation = Formation.query.filter_by(id_formation=identifiant).first()
            formation.intitule = intitule
            formation.niveau_qualif = niveau_qualif
            formation.groupe = groupe
            formation.image = image
            if commit:
                db.session.commit()
        except Exception as e:
            logging.error(f"Erreur lors de la modification de la formation {intitule}")
            logging.error(e)

    @staticmethod
    def archiver_formation(id_formation, archiver=True, commit=True):
        """
        Archive une formation en BD

        :param id_formation: id de la formation à archiver
        :param archiver: True pour archiver, False pour désarchiver
        :return: None
        """
        try:
            formation = Formation.query.filter_by(id_formation=id_formation).first()
            formation.archive = archiver
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            logging.error(f"Erreur lors de l'archivage de la formation {id_formation}")
            logging.error(e)
            return False

    @staticmethod
    def remove_formation(id_formation, commit=True):
        """
        Supprime une formation en BD

        :param id_formation: id de la formation à supprimer
        :return: None
        """
        try:
            for apprenti in Apprenti.get_apprentis_by_formation(id_formation):
                Apprenti.remove_apprenti(apprenti.id_apprenti)
            if commit:
                db.session.commit()
            for cours in Cours.get_cours_par_formation(id_formation):
                db.session.delete(cours)
            if commit:
                db.session.commit()
            db.session.delete(Formation.query.filter_by(id_formation=id_formation).first())
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la formation {id_formation}")
            logging.error(e)
            return False

    @staticmethod
    def reinitisaliser_formation(id_formation, commit=True):
        """
        Réinitialise une formation en retirant tous les apprentis et les cours d'une formation

        :param id_formation: id de la formation à réinitialiser
        :param commit: True pour commit, False pour ne pas commit
        :return: True si la réinitialisation s'est bien passée, False sinon
        """
        try:
            from custom_paquets.generation_xls import generer_xls_apprentis
            # Suppression des cours
            generer_xls_apprentis(id_formation)

            # Suppression des apprentis
            for apprenti in Apprenti.get_apprentis_by_formation(id_formation):
                Apprenti.remove_apprenti(apprenti.id_apprenti)

            if commit:
                db.session.commit()

            return True
        except Exception as e:
            logging.error(f"Erreur lors de la réinitisalisation de la formation {id_formation}")
            logging.error(e)
            return False
