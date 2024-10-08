from custom_paquets.converter import convert_to_dict
from custom_paquets.gestions_erreur import suplement_erreur
from custom_paquets.security import compare_passwords, encrypt_password
from model.composer import ComposerPresentation
from model.cours import Cours
from model.laissertrace import LaisserTrace
from model.shared_model import DB_SCHEMA, Assister, db


class Apprenti(db.Model):
    __tablename__ = "Apprenti"
    __table_args__ = {"schema": DB_SCHEMA}

    id_apprenti = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    mdp = db.Column(db.Text)
    photo = db.Column(db.String(100))
    essais = db.Column(db.Integer, nullable=False, default=0)
    archive = db.Column(db.Boolean, nullable=False, default=False)
    adaptation_situation_examen = db.Column(db.Text)

    @staticmethod
    def get_all_apprentis(archive=False):
        """
        Récupère l'id, nom, prenom et photo de chaque apprenti

        :return: La liste des apprentis
        """

        try:
            apprentis = (
                Apprenti.query.with_entities(Apprenti.id_apprenti, Apprenti.login, Apprenti.nom, Apprenti.prenom, Apprenti.photo, Apprenti.essais)
                .order_by(Apprenti.login)
                .filter(Apprenti.login != "dummy")
                .filter(Apprenti.archive == archive)
                .all()
            )
            return convert_to_dict(apprentis)
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la récupération des apprentis.")

    @staticmethod
    def get_adaptation_situation_examen_par_apprenti(login):
        """
        Récupère le commentaire de la CIP (adptation situation d'examen) de l'apprenti identifié par son login

        :return: Le commentaire de la CIP
        """
        try:
            return Apprenti.query.filter_by(login=login).with_entities(Apprenti.adaptation_situation_examen).first().adaptation_situation_examen
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la récupération de l'adaptation situation d'examen de l'apprenti " f"{login}")

    @staticmethod
    def update_adaptation_situation_examen_par_apprenti(login, adaptation_situation_examen):
        """
        Modifie le commentaire de la CIP (adaptation situation d'examen) de l'apprenti identifié par son login

        :return: True si l'opération s'est bien déroulée, False sinon
        """
        try:
            id_apprenti = Apprenti.get_id_apprenti_by_login(login)
            apprenti = Apprenti.query.filter_by(id_apprenti=id_apprenti).first()
            apprenti.adaptation_situation_examen = adaptation_situation_examen
            db.session.commit()
            return True
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la modification de l'adaptation situation d'examen de l'apprenti " f"{login}")
            return False

    @staticmethod
    def check_password_is_set(login: str):
        """
        Vérifie si le mot de passe d'un apprenti a bien été paramétré

        :param login: Login de l'apprenti
        :return: Un booleen si le mot de passe a été paramétré
        """
        try:
            return Apprenti.query.filter_by(login=login).first().mdp != "0000"
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la vérification du mot de passe de l'apprenti {login}")
            return False

    @staticmethod
    def get_apprenti_by_login(login: str):
        """
        Récupère les informations d'un apprenti à partir de son Login

        :return: Les informations de l'apprenti
        """
        try:
            return Apprenti.query.filter_by(login=login).with_entities(Apprenti.nom, Apprenti.prenom, Apprenti.login, Apprenti.id_apprenti).first()
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la récupération de l'apprenti {login}")

    @staticmethod
    def get_id_apprenti_by_login(login: str):
        """
        Renvoie l'id_apprenti à partir du login
        """
        try:
            return Apprenti.query.filter_by(login=login).with_entities(Apprenti.id_apprenti).first().id_apprenti
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la récupération de l'id de l'apprenti {login}")

    @staticmethod
    def get_login_apprenti_by_id(id_apprenti: str):
        """
        Renvoie l'id_apprenti à partir du login
        """
        try:
            return Apprenti.query.filter_by(id_apprenti=id_apprenti).with_entities(Apprenti.login).first().login
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la récupération du login de l'apprenti {id_apprenti}")

    @staticmethod
    def check_apprenti(login: str):
        """
        À partir d'un login, vérifie si un compte apprenti existe

        :return: Un booleen vrai si le compte existe
        """
        try:
            return Apprenti.query.filter_by(login=login).count() == 1
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la vérification de l'existence de l'apprenti {login}")
            return False

    @staticmethod
    def set_password_apprenti(login: str, new_password: str):
        """
        À partir d'un login et d'un mot de passe, modifie le mot de passe de l'apprenti

        :return: Un booleen vrai si le mot de passe a été modifié
        """
        try:
            apprenti = Apprenti.query.filter_by(login=login).first()
            apprenti.mdp = encrypt_password(new_password)
            db.session.commit()
            return True
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la modification du mot de passe de l'apprenti {login}")
            return False

    @staticmethod
    def check_password_non_set(login: str):
        """
        A partir d'un login, vérifie si le mot de passe de l'apprenti est à sa valeur par défaut

        :return: Un booleen vrai si le mot de passe est à sa valeur par défaut
        """
        return Apprenti.query.filter_by(login=login).first().mdp == "0000"

    @staticmethod
    def check_password_apprenti(login: str, new_password: str):
        """
        À partir d'un login et d'un mot de passe, vérifie si le mot de passe est valide
        Si le mot de passe est invalide, augmente le nombre d'essais de l'apprenti de 1

        :return: Ub booleen vrai si le mot de passe est valide
        """
        try:
            old_password = Apprenti.query.with_entities(Apprenti.mdp).filter_by(login=login).first().mdp
            digest = compare_passwords(new_password, old_password)
            if digest and Apprenti.get_nbr_essais_connexion_apprenti(login) < 5:
                Apprenti.reset_nbr_essais_connexion(login)
            elif not digest and Apprenti.get_nbr_essais_connexion_apprenti(login) < 5:
                Apprenti.update_nbr_essais_connexion(login)
            return digest
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la vérification du mot de passe de l'apprenti {login}")
            return False

    @staticmethod
    def get_nbr_essais_connexion_apprenti(login: str):
        """
        À partir d'un login, recupère le nombre de tentatives de connexion d'un apprenti

        :param login: LOGIN (ABC12) d'un apprenti
        :return: Un nombre allant de 0 à 5.
        """
        try:
            return Apprenti.query.filter_by(login=login).first().essais
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la récupération du nombre d'essais de connexion de l'apprenti {login}")

    @staticmethod
    def update_nbr_essais_connexion(login: str):
        """
        Augmente le nombre d'essais de connexion d'un apprenti de 1
        Limité à cinq essais.

        :return: Booleen en fonction de la réussite de l'opération
        """
        try:
            apprenti = Apprenti.query.filter_by(login=login).first()
            apprenti.essais = apprenti.essais + 1
            db.session.commit()
            return True
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la modification du nombre d'essais de connexion de l'apprenti {login}")
            return False

    @staticmethod
    def set_nbr_essais_connexion(login: str, nbr_essais: int):
        """
        Modifie le nombre d'essais de connexion d'un apprenti
        Limité à cinq essais.

        :return: Booleen en fonction de la réussite de l'opération
        """
        try:
            apprenti = Apprenti.query.filter_by(login=login).first()
            apprenti.essais = nbr_essais
            db.session.commit()
            return True
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la modification du nombre d'essais de connexion de l'apprenti {login}")
            return False

    @staticmethod
    def reset_nbr_essais_connexion(login: str):
        """
        Reset le nombre d'essais de connexion d'un apprenti à 0

        :return: Booleen en fonction de la réussite de l'opération
        """
        try:
            apprenti = Apprenti.query.filter_by(login=login).first()
            apprenti.essais = 0
            db.session.commit()
            return True
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la réinitialisation du nombre d'essais de connexion de l'apprenti {login}")
            return False

    @staticmethod
    def add_apprenti(nom, prenom, login, photo, commit=True):
        """
        Ajoute un apprenti en BD

        :return: id_apprenti
        """
        try:
            apprenti = Apprenti(nom=nom, prenom=prenom, login=login, photo=photo, mdp="0000")
            db.session.add(apprenti)
            if commit:
                db.session.commit()
            return Apprenti.get_id_apprenti_by_login(login)
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de l'ajout de l'apprenti {prenom} {nom}")

    @staticmethod
    def update_apprenti(identifiant, login, nom, prenom, photo, password, actif):
        """
        Modifie un apprenti en BD

        :return: None
        """
        try:
            apprenti = Apprenti.query.filter_by(id_apprenti=identifiant).first()
            apprenti.login = login
            apprenti.nom = nom
            apprenti.prenom = prenom
            apprenti.photo = photo
            if password:
                apprenti.mdp = "0000"
            if actif:
                apprenti.essais = 0
            else:
                apprenti.essais = 5
            db.session.commit()
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la modification de l'apprenti {prenom} {nom}")

    @staticmethod
    def archiver_apprenti(id_apprenti, archiver=True):
        """
        Archive un apprenti en BD

        :param id_apprenti: id de l'apprenti à archiver
        :param archiver: True pour archiver, False pour désarchiver
        :param commit: True pour commit, False pour ne pas commit
        :return: None
        """
        try:
            apprenti = Apprenti.query.filter_by(id_apprenti=id_apprenti).first()
            apprenti.archive = archiver
            db.session.commit()
            return True
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de l'archivage de l'apprenti {id_apprenti}")
            return False

    @staticmethod
    def remove_apprenti(id_apprenti, commit=True):
        """
        Supprime un apprenti en BD

        :param id_apprenti: id de l'apprenti à supprimer
        :param commit: True pour commit, False pour ne pas commit
        :return: None
        """
        try:
            from model.ficheintervention import FicheIntervention

            Assister.query.filter_by(id_apprenti=id_apprenti).delete()
            if commit:
                db.session.commit()
            fiches = FicheIntervention.query.filter_by(id_apprenti=id_apprenti).all()
            if fiches:
                for fiche in fiches:
                    ComposerPresentation.query.filter_by(id_fiche=fiche.id_fiche).delete()
                    LaisserTrace.query.filter_by(id_fiche=fiche.id_fiche).delete()
                for fiche in fiches:
                    db.session.delete(fiche)
            if commit:
                db.session.commit()
            db.session.delete(Apprenti.query.filter_by(id_apprenti=id_apprenti).first())
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            suplement_erreur(e, message=f"Erreur lors de la suppression de l'apprenti {id_apprenti}")
            return False

    @staticmethod
    def get_apprentis_by_formation(id_formation):
        """
        Récupère les apprentis d'une formation
        """
        try:
            return Apprenti.query.join(Assister).join(Cours).filter_by(id_formation=id_formation).all()
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la récupération des apprentis de la formation.")

    @staticmethod
    def get_apprentis_for_xls(id_formation):
        """
        Récupère les apprentis d'une formation
        """
        try:
            return (
                Apprenti.query.with_entities(Apprenti.nom, Apprenti.prenom, Apprenti.login, Apprenti.adaptation_situation_examen)
                .join(Assister)
                .join(Cours)
                .filter_by(id_formation=id_formation)
                .distinct()
                .all()
            )
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la récupération des apprentis de la formation.")

    @staticmethod
    def get_photos_profil_apprenti(id_apprenti):
        try:
            return Apprenti.query.filter_by(id_apprenti=id_apprenti).with_entities(Apprenti.photo).first().photo
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la récupération de la photo de profil de l'apprenti.")
