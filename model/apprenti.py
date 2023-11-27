from hmac import compare_digest

from custom_paquets.converter import convert_to_dict
from custom_paquets.security import encrypt_password

from model_db.shared_model import db
from model_db.apprenti import Apprenti

from model_db.ficheintervention import FicheIntervention


def get_all_apprenti():
    """
    Récupère l'id, nom, prenom et photo de chaque apprenti

    :return: La liste des apprentis
    """
    apprenti = Apprenti.query.with_entities(
        Apprenti.id_apprenti, Apprenti.login, Apprenti.nom, Apprenti.prenom, Apprenti.photo, Apprenti.essaies
    ).order_by(Apprenti.login).filter(Apprenti.login != "dummy").all()
    return convert_to_dict(apprenti)


def get_apprenti_by_login(login: str):
    """
    Recupere les informations d'un apprenti à partir de son Login

    :return: Les informations de l'apprenti
    """
    return convert_to_dict(Apprenti.query.filter_by(login=login).with_entities(Apprenti.nom, Apprenti.prenom,
                                                                               Apprenti.login).all())


def get_id_apprenti_by_login(login: str):
    """
    Renvoie l'id_apprenti à partir du login
    """
    return convert_to_dict(Apprenti.query.filter_by(login=login).with_entities(Apprenti.id_apprenti).first())


def check_password_apprenti(login: str, password: str):
    """
    À partir d'un login et d'un mot de passe, verifie si le mot de passe est valide

    :return: Ub booleen vrai si le mot de passe est valide
    """
    passwd = Apprenti.query.with_entities(Apprenti.mdp).filter_by(login=login).first().mdp
    return compare_digest(encrypt_password(password, login), passwd)


def get_nbr_essaie_connexion_apprenti(login: str):
    """
    A partir d'un login, recupère le nombre d'essaie de connexion d'un apprenti

    :param login: LOGIN (ABC12) d'un apprenti
    :return: UN nombre allant de 0 à 5
    """
    return Apprenti.query.filter_by(login=login).first().essaies
