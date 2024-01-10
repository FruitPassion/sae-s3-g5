import urllib.parse

from flask import Blueprint, jsonify

from custom_paquets.decorateur import admin_login_required
from model.apprenti import check_password_apprenti, get_nbr_essais_connexion_apprenti, archiver_apprenti, \
    remove_apprenti, set_password_apprenti
from model.formation import archiver_formation, remove_formation, reinitisaliser_formation
from model.personnel import archiver_personnel, remove_personnel
from model.cours import archiver_cours, remove_cours

api = Blueprint('api', __name__, url_prefix="/api")

'''
Blueprint pour toutes les routes relatives aux URL d'API

Préfixe d'URL : /api/ .
'''


@api.route("/check-password-apprenti/<user>/<password>", methods=["GET"])
def api_check_password_apprenti(user, password):
    """
    Vérifie que le login et le password correspondent bien à ceux de la base de données
    """
    if get_nbr_essais_connexion_apprenti(user) != 5:
        return {"valide": check_password_apprenti(user, password)}
    else:
        return {"blocage": True}


@api.route("/set-password-apprenti/<user>/<password>", methods=["GET"])
def api_set_password_apprenti(user, password):
    """
    Modifie le mot de passe d'un apprenti

    :param user: Login de l'apprenti
    :param password: Nouveau mot de passe
    """
    if check_password_apprenti(user, password):
        return {"valide": False}
    else:
        return {"valide": set_password_apprenti(user, password)}


@api.route("/archiver-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_archiver_formation(id_formation, commit=True):
    """
    Archive une formation à partir de son id
    """
    return {"valide": archiver_formation(id_formation, commit=commit), "retirer": True}


@api.route("/reinitialiser-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_reinitialiser_formation(id_formation, commit=True):
    """
    Réinitialise une formation à partir de son id

    :param id_formation:
    :param commit:
    :return: JSON valide
    """
    return {"valide": reinitisaliser_formation(id_formation, commit=commit)}


@api.route("/desarchiver-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_desarchiver_formation(id_formation):
    """
    Désarchive une formation à partir de son id

    :param id_formation:
    :return: JSON valide
    """
    return {"valide": archiver_formation(id_formation, archiver=False)}


@api.route("/supprimer-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_supprimer_formation(id_formation):
    """
    Supprime une formation à partir de son id
    """
    return {"valide": remove_formation(id_formation)}


@api.route("/archiver-apprenti/<id_apprenti>", methods=["GET"])
@admin_login_required
def api_archiver_apprenti(id_apprenti):
    """
    Archive un apprenti à partir de son id
    """
    return {"valide": archiver_apprenti(id_apprenti), "retirer": True}


@api.route("/desarchiver-apprenti/<id_apprenti>", methods=["GET"])
@admin_login_required
def api_desarchiver_apprenti(id_apprenti):
    """
    Désarchive un apprenti à partir de son id
    """
    return {"valide": archiver_apprenti(id_apprenti, archiver=False)}


@api.route("/supprimer-apprenti/<id_apprenti>", methods=["GET"])
@admin_login_required
def api_supprimer_apprenti(id_apprenti):
    """
    Supprime un apprenti à partir de son id
    """
    return {"valide": remove_apprenti(id_apprenti)}


@api.route("/archiver-cours/<id_cours>", methods=["GET"])
@admin_login_required
def api_archiver_cours(id_cours):
    """
    Archive un cours à partir de son id
    """
    return {"valide": archiver_cours(id_cours), "retirer": True}


@api.route("/desarchiver-cours/<id_cours>", methods=["GET"])
@admin_login_required
def api_desarchiver_cours(id_cours):
    """
    Désarchive un cours à partir de son id
    """
    return {"valide": archiver_cours(id_cours, archiver=False)}


@api.route("/supprimer-cours/<id_cours>", methods=["GET"])
@admin_login_required
def api_supprimer_cours(id_cours):
    """
    Supprime un cours à partir de son id
    """
    return {"valide": remove_cours(id_cours)}


@api.route("/archiver-personnel/<id_personnel>", methods=["GET"])
@admin_login_required
def api_archiver_personnel(id_personnel):
    """
    Archive un personnel à partir de son id
    """
    return {"valide": archiver_personnel(id_personnel), "retirer": True}


@api.route("/desarchiver-personnel/<id_personnel>", methods=["GET"])
@admin_login_required
def api_desarchiver_personnel(id_personnel):
    """
    Désarchive un personnel à partir de son id
    """
    return {"valide": archiver_personnel(id_personnel, archiver=False)}


@api.route("/supprimer-personnel/<id_personnel>", methods=["GET"])
@admin_login_required
def api_supprimer_personnel(id_personnel):
    """
    Supprime un personnel à partir de son id
    """
    return {"valide": remove_personnel(id_personnel)}