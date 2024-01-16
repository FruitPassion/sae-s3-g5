import logging

from custom_paquets.converter import convert_to_dict
from custom_paquets.security import compare_passwords

from model.shared_model import db, Personnel, LaisserTrace, EducAdmin, FicheIntervention


def get_all_personnel(archive=False):
    """
    Récupère l'id, nom, prenom et rôle de chaque membre du personnel

    :return: La liste des membres du personnel
    """
    try:
        return Personnel.query.order_by(Personnel.login).filter(
            Personnel.archive == archive).filter(Personnel.role != "dummy").all()
    except Exception as e:
        logging.error("Erreur lors de la récupération de la liste de tout le personnel")
        logging.error(e)


def get_liste_personnel_non_super(archive=False):
    try:
        return Personnel.query.with_entities(Personnel.id_personnel, Personnel.login).filter(
            Personnel.role != "SuperAdministrateur").filter(Personnel.archive == archive).filter(
            Personnel.role != "dummy").all()
    except Exception as e:
        logging.error("Erreur lors de la récupération de la liste du personnel sans l'admin")
        logging.error(e)


def get_id_personnel_by_login(login: str):
    """
    Renvoie l'id_personnel à partir du login
    """
    try:
        return Personnel.query.filter_by(login=login).with_entities(Personnel.id_personnel).first().id_personnel
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'id_personnel de {login}")
        logging.error(e)


def check_super_admin(login: str):
    """
    À partir d'un login, vérifie si un compte possède le rôle superadmin.

    :return: Un booleen vrai si l'username appartient à un compte superadmin
    """
    try:
        return Personnel.query.with_entities(Personnel.role).filter_by(
            login=login).first().role == "SuperAdministrateur"
    except AttributeError as e:
        logging.error("Erreur lors de la vérification du superadmin")
        return False


def check_personnel(login: str):
    """
    À partir d'un login, vérifie si un compte existe

    :return: Un booleen vrai si le compte existe
    """
    return Personnel.query.filter_by(login=login).count() == 1


def get_role_by_login(login: str):
    """
    À partir d'un login récupère le rôle

    :return: Un rôle
    """
    try:
        return Personnel.query.filter_by(login=login).with_entities(
            Personnel.role).first().role
    except AttributeError as e:
        logging.error(f"Erreur lors de la récupération du role de {login}")
        return None


def check_password(login: str, new_password: str):
    """
    À partir d'un login et d'un mot de passe, vérifie si le mot de passe est valide

    :return: Un booleen vrai si le mot de passe est valide
    """
    try:
        old_password = Personnel.query.with_entities(Personnel.mdp).filter_by(login=login).first().mdp
        digest = compare_passwords(new_password, old_password)
        if digest and get_nbr_essais_connexion_personnel(login) < 3:
            reset_nbr_essais_connexion(login)
        elif not digest and get_nbr_essais_connexion_personnel(login) < 3:
            update_nbr_essais_connexion(login)
        return digest
    except Exception as e:
        logging.error(f"Erreur lors de la vérification du mot de passe de {login}")
        logging.error(e)


def get_nbr_essais_connexion_personnel(login: str):
    """
    À partir d'un login, recupère le nombre d'essais de connexion d'un personnel

    :param login: LOGIN (ABC12) d'un personnel
    :return: UN nombre allant de 0 à 3
    """
    try:
        return Personnel.query.filter_by(login=login).first().essais
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du nombre d'essais de connexion de {login}")
        logging.error(e)


def update_nbr_essais_connexion(login: str):
    """
    Augmente le nombre d'essais de connexion d'un personnel de 1
    Limité à 3

    :return: Booleen en fonction de la réussite de l'opération
    """
    personnel = Personnel.query.filter_by(login=login).first()
    personnel.essais = personnel.essais + 1
    try:
        db.session.commit()
        return True
    except:
        return False


def reset_nbr_essais_connexion(login: str):
    """
    Reset le nombre d'essais de connexion d'un personnel à 0

    :return: Booleen en fonction de la réussite de l'opération
    """
    personnel = Personnel.query.filter_by(login=login).first()
    personnel.essais = 0
    try:
        db.session.commit()
        return True
    except:
        return False


def add_personnel(login, nom, prenom, email, password, role, commit=True):
    """
    Ajoute un membre du personnel en BD

    :return: None
    """
    try:
        personnel = Personnel(login=login, nom=nom, prenom=prenom, email=email, mdp=password, role=role)
        db.session.add(personnel)
        if commit:
            db.session.commit()
        return get_id_personnel_by_login(login)
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout de {prenom} {nom}")
        logging.error(e)


def update_personnel(identifiant, login, nom, prenom, email, role, actif=None, password=None, commit=True):
    """
    Modifie un membre du personnel en BD

    :return: None
    """
    try:
        personnel = Personnel.query.filter_by(id_personnel=identifiant).first()

        personnel.login = login
        personnel.nom = nom
        personnel.prenom = prenom
        personnel.email = email
        personnel.role = role
        if password is not None:
            personnel.mdp = password
        if actif:
            personnel.essais = 0
        elif actif == False:
            personnel.essais = 3
        if commit:
            db.session.commit()

    except Exception as e:
        logging.error(f"Erreur lors de la modification de {prenom} {nom}")
        logging.error(e)


def archiver_personnel(id_personnel: int, archiver=True, commit=True):
    """
    Archive un membre du personnel

    :param id_personnel: id du membre du personnel à archiver
    :param archiver: True pour archiver, False pour désarchiver
    :param commit: True pour commit, False pour ne pas commit
    :return: Booleen en fonction de la réussite de l'opération
    """
    try:
        personnel = Personnel.query.filter_by(id_personnel=id_personnel).first()
        personnel.archive = archiver
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur lors de l'archivage du personnel {id_personnel}")
        logging.error(e)
        return False


def remove_personnel(id_personnel: int, commit=True):
    """
    Supprime un membre du personnel en l'anonymisant (dummy)
    Remplace toute les référence à son id en base de données par celle du personnel dummy

    :param id_personnel: id du membre du personnel à supprimer
    :param commit: True pour commit, False pour ne pas commit
    :return: Booléen en fonction de la réussite de l'opération
    """
    try:
        # Retirer le personnel des traces
        traces = LaisserTrace.query.filter_by(id_personnel=id_personnel).all()
        if traces:
            for trace in traces:
                trace.id_personnel = 1

        # Retirer le personnel des fiches d'intervention
        fiches = FicheIntervention.query.filter_by(id_personnel=id_personnel).all()
        if fiches:
            for fiche in fiches:
                fiche.id_personnel = 1

        if commit:
            db.session.commit()

        # Retirer le personnel des Educateur Administrateur
        educ_admin = EducAdmin.query.filter_by(id_personnel=id_personnel).first()
        if educ_admin:
            db.session.delete(educ_admin)

        if commit:
            db.session.commit()

        # Supprimer le personnel
        personnel = Personnel.query.filter_by(id_personnel=id_personnel).first()
        db.session.delete(personnel)
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la suppression du personnel {id_personnel}")
        logging.error(e)
        return False
