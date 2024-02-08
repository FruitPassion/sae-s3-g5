import logging

from model.shared_model import db, DB_SCHEMA, Assister



class Cours(db.Model):
    __tablename__ = 'Cours'
    __table_args__ = {'schema': DB_SCHEMA}

    id_cours = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(50), nullable=False)
    cours = db.Column(db.String(50), nullable=False)
    duree = db.Column(db.Integer)
    archive = db.Column(db.Boolean, nullable=False, default=False)
    id_formation = db.Column(db.ForeignKey(f'{DB_SCHEMA}.Formation.id_formation'), nullable=False, index=True)

    Formation = db.relationship('Formation', primaryjoin='Cours.id_formation == Formation.id_formation',
                                backref='cours')

    @staticmethod
    def get_all_cours(archive=False):
        """
        Retourne la liste de tous les cours

        :return: Une liste des cours
        """
        try:
            return Cours.query.filter(Cours.archive == archive).all()
        except Exception as e:
            logging.error("Erreur lors de la récupération de tous les cours")
            logging.error(e)

    @staticmethod
    def get_liste_cours_assister(id_apprenti, archive=False):
        """
        Retourne la liste de tous les cours

        :return: Une liste des cours
        """
        try:
            return Cours.query.with_entities(Cours.cours).filter(Cours.archive == archive).join(
                Assister).filter_by(id_apprenti=id_apprenti).distinct().all()
        except Exception as e:
            logging.error("Erreur lors de la récupération de tous les cours")
            logging.error(e)

    @staticmethod
    def get_apprentis_by_formation(nom_formation: str, archive=False):
        """
        Retourne la liste de tous les apprentis inscrits à une formation

        :return: Une liste d'apprentis
        """
        try:
            from model.formation import Formation
            from model.apprenti import Apprenti
            return Cours.query.distinct().filter_by(
                id_formation=Formation.get_formation_id_par_nom_formation(nom_formation)).join(
                Assister).join(Apprenti).with_entities(Apprenti.nom, Apprenti.prenom, Apprenti.login,
                                                       Apprenti.photo).filter(Apprenti.archive == archive).all()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des apprentis de la formation {nom_formation}")
            logging.error(e)

    @staticmethod
    def get_cours_par_apprenti(id_apprenti):
        """
        Retourne la liste de tous les cours auxquels un apprenti est inscrit

        :return: Une liste de cours
        """
        try:
            return Cours.query.with_entities(Cours.theme, Cours.cours, Cours.id_cours).join(Assister).filter_by(
                id_apprenti=id_apprenti).all()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des cours de l'apprenti {id_apprenti}")
            logging.error(e)

    @staticmethod
    def add_apprenti_assister(id_apprenti, id_formation):
        """
        Associe un apprenti à un cours en BD

        :return: None
        """
        try:
            cours = Cours.get_cours_par_formation(id_formation)
            for un_cour in cours:
                assister = Assister(id_apprenti=id_apprenti, id_cours=un_cour.id_cours)
                db.session.add(assister)
            db.session.commit()
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout de l'apprenti {id_apprenti} à la formation {id_formation}")
            logging.error(e)

    @staticmethod
    def get_cours_par_formation(id_formation):
        """
        :return: tous les cours de la formation id_formation
        """
        try:
            return Cours.query.filter_by(id_formation=id_formation).all()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des cours de la formation {id_formation}")
            logging.error(e)

    @staticmethod
    def get_id_cours_by_theme(theme):
        """
        Retourne l'id d'un cours en fonction de son thème

        :return: id_cours
        """
        try:
            return Cours.query.filter_by(theme=theme).first().id_cours
        except Exception as e:
            logging.error("Erreur lors de la récupération de l'id du cours")
            logging.error(e)

    def get_cours_id(nom_cours: str):
        """
        Retourne l'id d'un cours à partir de son nom

        :return: Un id de cours
        """
        try:
            return Cours.query.with_entities(Cours.id_cours).filter_by(cours=nom_cours).first().id_cours
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'id du cours {nom_cours}")
            logging.error(e)

    @staticmethod
    def get_nom_cours_by_id(id_cours):
        """
        Retourne le nom d'un cours à partir de son id

        :return: Un nom de cours
        """
        try:
            return Cours.query.with_entities(Cours.cours).filter_by(id_cours=id_cours).first().cours
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du nom du cours {id_cours}")
            logging.error(e)

    @staticmethod
    def add_cours(theme, cours, duree, id_formation, commit=True):
        """
        Ajoute un cours en BD

        :return: id_cours
        """
        try:
            cours_ajoute = Cours(theme=theme, cours=cours, duree=duree, id_formation=id_formation)
            db.session.add(cours_ajoute)
            if commit:
                db.session.commit()
            return Cours.get_cours_id(cours)
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du cours {cours}")
            logging.error(e)

    @staticmethod
    def update_cours(identifiant, theme, intitule, duree, id_formation, commit=True):
        """
        Modifie un cours en BD

        :return: None
        """
        try:
            cours = Cours.query.filter_by(id_cours=identifiant).first()
            cours.theme = theme
            cours.cours = intitule
            cours.duree = duree
            cours.id_formation = id_formation
            if commit:
                db.session.commit()
        except Exception as e:
            logging.error(f"Erreur lors de la modification du cours {intitule}")
            logging.error(e)

    @staticmethod
    def archiver_cours(id_cours, archiver=True, commit=True):
        """
        Archive un cours en BD

        :return: un boolean (True si l'archivage s'est bien passé, False sinon)
        """
        try:
            cours = Cours.query.filter_by(id_cours=id_cours).first()
            cours.archive = archiver
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            logging.error(f"Erreur lors de l'archivage du cours {id_cours}")
            logging.error(e)
            return False

    @staticmethod
    def remove_cours(id_cours, commit=True):
        """
        Supprime un cours en BD

        :return: None
        """
        try:
            assister = Assister.query.filter_by(id_cours=id_cours).all()
            for a in assister:
                db.session.delete(a)
            if commit:
                db.session.commit()
            db.session.delete(Cours.query.filter_by(id_cours=id_cours).first())
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du cours {id_cours}")
            logging.error(e)
            return False
