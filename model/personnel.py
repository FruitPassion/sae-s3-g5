from hmac import compare_digest

from custom_paquets.converter import convertToDict
from custom_paquets.security import encryptPassword

from model_db.shared_model import db
from model_db.personnel import Personnel


def getAllPersonnel():
    """
    Récupère l'id, nom, prenom et role de chaque membre du personnel

    :return: La liste des membres du personnel
    """
    personnel = (Personnel.query.with_entities(Personnel.id_personnel, Personnel.nom, Personnel.prenom, Personnel.role).
                 all())
    return convertToDict(personnel)


def checkSuperAdmin(login: str):
    """
    À partir d'un login, verifie si un compte possède le role superadmin.

    :return: Ub booleen vrai si l'username appartient à un compte superadmin
    """
    return Personnel.query.with_entities(Personnel.role).query.filter_by(login=login).first().role == "SuperAdministrateur"


def checkPersonnel(login: str):
    """
    À partir d'un login, verifie si un compte existe

    :return: Ub booleen vrai si le compte existe
    """
    return Personnel.query.filter_by(login=login).count() == 1


def checkPassword(login: str, password: str):
    passwd = Personnel.query.with_entities(Personnel.mdp).filter_by(login=login).first().mdp
    return compare_digest(encryptPassword(password, login), passwd)
