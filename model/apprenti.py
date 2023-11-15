from hmac import compare_digest

from custom_paquets.converter import convert_to_dict
from custom_paquets.security import encrypt_password

from model_db.shared_model import db
from model_db.apprenti import Apprenti


def get_apprenti_by_login(login: str):
    """
    Recupere les informations d'un apprenti a partir de son Login

    :return: Les informations de l'apprenti
    """
    return convert_to_dict(Apprenti.query.filter_by(login=login).with_entities(Apprenti.nom, Apprenti.prenom,
                                                                               Apprenti.login).all())


def check_password_apprenti(login: str, password: str):
    """
    À partir d'un login et d'un mot de passe, verifie si le mot de passe est valide

    :return: Ub booleen vrai si le mot de passe est valide
    """
    passwd = Apprenti.query.with_entities(Apprenti.mdp).filter_by(login=login).first().mdp
    return compare_digest(encrypt_password(password, login), passwd)