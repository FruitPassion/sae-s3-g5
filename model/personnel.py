import logging
from hmac import compare_digest

from custom_paquets.converter import convert_to_dict
from custom_paquets.security import encrypt_password

from model_db.shared_model import db
from model_db.personnel import Personnel


def get_all_personnel():
    """
    Récupère l'id, nom, prenom et role de chaque membre du personnel

    :return: La liste des membres du personnel
    """
    personnel = Personnel.query.with_entities(
        Personnel.id_personnel, Personnel.login, Personnel.nom, Personnel.prenom, Personnel.role, Personnel.email,
        Personnel.essaies).order_by(Personnel.login).all()
    return convert_to_dict(personnel)


def check_super_admin(login: str):
    """
    À partir d'un login, verifie si un compte possède le role superadmin.

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
    À partir d'un login, verifie si un compte existe

    :return: Un booleen vrai si le compte existe
    """
    return Personnel.query.filter_by(login=login).count() == 1


def get_role(login: str):
    """
    À partir d'un login recupere le role

    :return: Un role
    """
    try:
        return Personnel.query.filter_by(login=login).with_entities(
            Personnel.role
        ).first().role
    except AttributeError as e:
        logging.error("Erreur lors de la récupération du role")
        return None


def check_password(login: str, password: str):
    """
    À partir d'un login et d'un mot de passe, verifie si le mot de passe est valide

    :return: Un booleen vrai si le mot de passe est valide
    """
    passwd = (
        Personnel.query.with_entities(Personnel.mdp)
        .filter_by(login=login)
        .first()
        .mdp
    )
    digest = compare_digest(encrypt_password(password, login), passwd)
    if digest and get_nbr_essaie_connexion_personnel(login) < 3:
        reset_nbr_essaies_connexion(login)
    elif not digest and get_nbr_essaie_connexion_personnel(login) < 3:
        update_nbr_essaies_connexion(login)
    return digest


def get_nbr_essaie_connexion_personnel(login: str):
    """
    A partir d'un login, recupère le nombre d'essaie de connexion d'un personnel

    :param login: LOGIN (ABC12) d'un personnel
    :return: UN nombre allant de 0 à 3
    """
    return Personnel.query.filter_by(login=login).first().essaies


def update_nbr_essaies_connexion(login: str):
    """
    Augmente le nombre d'essaies de connexion d'un personnel de 1
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
    Reset le nombre d'essaies de connexion d'un personnel a 0

    :return: Booleen en fonction de la réussite de l'opération
    """
    personnel = Personnel.query.filter_by(login=login).first()
    personnel.essaies = 0
    try:
        db.session.commit()
        return True
    except:
        return False
