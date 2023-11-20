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
        Personnel.id_personnel, Personnel.nom, Personnel.prenom, Personnel.role
    ).all()
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
        raise e


def check_personnel(login: str):
    """
    À partir d'un login, verifie si un compte existe

    :return: Un booleen vrai si le compte existe
    """
    return Personnel.query.filter_by(login=login).count() == 1


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
    return compare_digest(encrypt_password(password, login), passwd)


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
        raise e
