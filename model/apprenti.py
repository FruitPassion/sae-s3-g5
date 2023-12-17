import logging
from hmac import compare_digest

from custom_paquets.converter import convert_to_dict
from custom_paquets.security import encrypt_password, compare_passwords

from model_db.shared_model import db
from model_db.apprenti import Apprenti

from model_db.ficheintervention import FicheIntervention
from model.formation import get_nom_formation


def get_all_apprenti(archive=False):
    """
    Récupère l'id, nom, prenom et photo de chaque apprenti

    :return: La liste des apprentis
    """
    apprenti = Apprenti.query.with_entities(
        Apprenti.id_apprenti, Apprenti.login, Apprenti.nom, Apprenti.prenom, Apprenti.photo, Apprenti.essaies
    ).order_by(Apprenti.login).filter(Apprenti.login != "dummy").filter(Apprenti.archive == archive).all()
    return convert_to_dict(apprenti)


def get_apprenti_by_login(login: str):
    """
    Recupere les informations d'un apprenti à partir de son Login

    :return: Les informations de l'apprenti
    """
    return convert_to_dict(Apprenti.query.filter_by(login=login).with_entities(Apprenti.nom, Apprenti.prenom,
                                                                               Apprenti.login).all())[0]


def get_id_apprenti_by_login(login: str):
    """
    Renvoie l'id_apprenti à partir du login
    """
    return Apprenti.query.filter_by(login=login).with_entities(Apprenti.id_apprenti).first().id_apprenti


def check_apprenti(login: str):
    """
    À partir d'un login, verifie si un compte existe

    :return: Un booleen vrai si le compte existe
    """
    return Apprenti.query.filter_by(login=login).count() == 1


def check_password_apprenti(login: str, new_password: str):
    """
    À partir d'un login et d'un mot de passe, verifie si le mot de passe est valide
    Si le mot de passe est invalide, augmmente le nombre d'essaie de l'apprenti de 1

    :return: Ub booleen vrai si le mot de passe est valide
    """
    old_password = Apprenti.query.with_entities(Apprenti.mdp).filter_by(login=login).first().mdp
    digest = compare_passwords(new_password, old_password)
    if digest and get_nbr_essaie_connexion_apprenti(login) < 5:
        reset_nbr_essaies_connexion(login)
    elif not digest and get_nbr_essaie_connexion_apprenti(login) < 5:
        update_nbr_essaies_connexion(login)
    return digest


def get_nbr_essaie_connexion_apprenti(login: str):
    """
    À partir d'un login, recupère le nombre d'essayer de connexion d'un apprenti

    :param login: LOGIN (ABC12) d'un apprenti
    :return: UN nombre allant de 0 à 5
    """
    return Apprenti.query.filter_by(login=login).first().essaies


def update_nbr_essaies_connexion(login: str):
    """
    Augmente le nombre d'essaies de connexion d'un apprenti de 1
    Limité à 5

    :return: Booleen en fonction de la réussite de l'opération
    """
    apprenti = Apprenti.query.filter_by(login=login).first()
    apprenti.essaies = apprenti.essaies + 1
    try:
        db.session.commit()
        return True
    except:
        return False


def reset_nbr_essaies_connexion(login: str):
    """
    Reset le nombre d'essaie de connexion d'un apprenti a 0

    :return: Booleen en fonction de la réussite de l'opération
    """
    apprenti = Apprenti.query.filter_by(login=login).first()
    apprenti.essaies = 0
    try:
        db.session.commit()
        return True
    except:
        return False


def add_apprenti(nom, prenom, login, photo):
    """
    Ajoute un apprenti en BD

    :return: id_apprenti
    """
    apprenti = Apprenti(nom=nom, prenom=prenom, login=login, photo=photo)
    db.session.add(apprenti)
    db.session.commit()
    return apprenti.id_apprenti


def archiver_apprenti(id_apprenti, archiver=True):
    """
    Archive un apprenti en BD

    :param id_apprenti: id de l'apprenti à archiver
    :param archiver: True pour archiver, False pour désarchiver
    :return: None
    """
    try:
        apprenti = Apprenti.query.filter_by(id_apprenti=id_apprenti).first()
        apprenti.archive = archiver
        db.session.commit()
        return True
    except AttributeError as e:
        logging.error("Erreur lors de l'archivage d'un apprenti")
        return False
