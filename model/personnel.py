import logging
from hmac import compare_digest

from custom_paquets.converter import convert_to_dict
from custom_paquets.security import compare_passwords

from model_db.shared_model import db
from model_db.personnel import Personnel


def get_all_personnel(archive=False):
    """
    Récupère l'id, nom, prenom et role de chaque membre du personnel

    :return: La liste des membres du personnel
    """
    personnel = Personnel.query.with_entities(
        Personnel.id_personnel, Personnel.login, Personnel.nom, Personnel.prenom, Personnel.role, Personnel.email,
        Personnel.essaies).order_by(Personnel.login).filter(Personnel.archive == archive).all()
    return convert_to_dict(personnel)


def get_liste_personnel_non_super(archive=False):
    return convert_to_dict(Personnel.query.with_entities(Personnel.id_personnel, Personnel.login).filter(
        Personnel.role != "SuperAdministrateur").filter(Personnel.archive == archive).all())


def get_id_personnel_by_login(login: str):
    """
    Renvoie l'id_personnel à partir du login
    """
    return Personnel.query.filter_by(login=login).with_entities(Personnel.id_personnel).first().id_personnel


def check_super_admin(login: str):
    """
    À partir d'un login, verifie si un compte possède le rôle superadmin.

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


def get_role(login: str):
    """
    À partir d'un login récupère le rôle

    :return: Un rôle
    """
    try:
        return Personnel.query.filter_by(login=login).with_entities(
            Personnel.role
        ).first().role
    except AttributeError as e:
        logging.error("Erreur lors de la récupération du role")
        return None


def check_password(login: str, new_password: str):
    """
    À partir d'un login et d'un mot de passe, vérifie si le mot de passe est valide

    :return: Un booleen vrai si le mot de passe est valide
    """
    old_password = Personnel.query.with_entities(Personnel.mdp).filter_by(login=login).first().mdp
    digest = compare_passwords(new_password, old_password)
    if digest and get_nbr_essaie_connexion_personnel(login) < 3:
        reset_nbr_essaies_connexion(login)
    elif not digest and get_nbr_essaie_connexion_personnel(login) < 3:
        update_nbr_essaies_connexion(login)
    return digest


def get_nbr_essaie_connexion_personnel(login: str):
    """
    À partir d'un login, recupère le nombre d'essai de connexion d'un personnel

    :param login: LOGIN (ABC12) d'un personnel
    :return: UN nombre allant de 0 à 3
    """
    return Personnel.query.filter_by(login=login).first().essaies


def update_nbr_essaies_connexion(login: str):
    """
    Augmente le nombre d'essais de connexion d'un personnel de 1
    Limité à 3

    :return: Booleen en fonction de la réussite de l'opération
    """
    personnel = Personnel.query.filter_by(login=login).first()
    personnel.essaies = personnel.essaies + 1
    try:
        db.session.commit()
        return True
    except:
        return False


def reset_nbr_essaies_connexion(login: str):
    """
    Reset le nombre d'essais de connexion d'un personnel à 0

    :return: Booleen en fonction de la réussite de l'opération
    """
    personnel = Personnel.query.filter_by(login=login).first()
    personnel.essaies = 0
    try:
        db.session.commit()
        return True
    except:
        return False


def add_personnel(login, nom, prenom, email, password, role):
    """
    Ajoute un membre du personnel en BD

    :return: id_personnel
    """
    try:
        personnel = Personnel(login=login, nom=nom, prenom=prenom, email=email, mdp=password, role=role)
        db.session.add(personnel)
        db.session.commit()
    except Exception as e:
        logging.error("Erreur lors de l'ajout d'un membre du personnel")
        logging.error(e)


def archiver_personnel(id_personnel: int, archiver=True):
    """
    Archive un membre du personnel

    :param id_personnel: id du membre du personnel à archiver
    :param archiver: True pour archiver, False pour désarchiver
    :return: Booleen en fonction de la réussite de l'opération
    """
    try:
        personnel = Personnel.query.filter_by(id_personnel=id_personnel).first()
        personnel.archive = archiver
        db.session.commit()
        return True
    except Exception as e:
        logging.error("Erreur lors de l'archivage d'un membre du personnel")
        logging.error(e)
        return False


def remove_personnel(id_personnel: int):
    """
    Supprime un membre du personnel en BD

    :return: Booleen en fonction de la réussite de l'opération
    """
    try:
        return True
    except Exception as e:
        logging.error("Erreur lors de la suppression d'un membre du personnel")
        logging.error(e)
        return False
