import urllib.parse

from flask import Blueprint, jsonify

from custom_paquets.decorateur import admin_login_required
from model.apprenti import check_password_apprenti, get_nbr_essaie_connexion_apprenti, archiver_apprenti, \
    remove_apprenti, archiver_apprentis_formation, set_password_apprenti
from model.formation import archiver_formation, remove_formation
from model.personnel import archiver_personnel

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
    essaies = get_nbr_essaie_connexion_apprenti(user)
    if essaies != 5:
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
    Archiver une formation à partir de son id
    """
    return {"valide": archiver_formation(id_formation, commit=commit), "retirer": True}


@api.route("/archiver-apprentis-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_archiver_apprentis_formation(id_formation, commit=True):
    """
    Archiver tous les apprentis d'une formation à partir de son id
    """
    return {"valide": archiver_apprentis_formation(id_formation, commit=commit), "retirer": False}


@api.route("/desarchiver-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_desarchiver_formation(id_formation):
    """
    Désarchiver une formation à partir de son id
    """
    return {"valide": archiver_formation(id_formation, archiver=False)}


@api.route("/supprimer-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_supprimer_formation(id_formation):
    """
    Supprimer une formation à partir de son id
    """
    return {"valide": remove_formation(id_formation)}


@api.route("/archiver-apprenti/<id_apprenti>", methods=["GET"])
@admin_login_required
def api_archiver_apprenti(id_apprenti):
    """
    Archiver un apprenti à partir de son id
    """
    return {"valide": archiver_apprenti(id_apprenti), "retirer": True}


@api.route("/desarchiver-apprenti/<id_apprenti>", methods=["GET"])
@admin_login_required
def api_desarchiver_apprenti(id_apprenti):
    """
    Désarchiver un apprenti à partir de son id
    """
    return {"valide": archiver_apprenti(id_apprenti, archiver=False)}


@api.route("/supprimer-apprenti/<id_apprenti>", methods=["GET"])
@admin_login_required
def api_supprimer_apprenti(id_apprenti):
    """
    Supprimer un apprenti à partir de son id
    """
    return {"valide": remove_apprenti(id_apprenti)}


@api.route("/archiver-personnel/<id_personnel>", methods=["GET"])
@admin_login_required
def api_archiver_personnel(id_personnel):
    """
    Archiver un personnel à partir de son id
    """
    return {"valide": archiver_personnel(id_personnel), "retirer": True}


@api.route("/desarchiver-personnel/<id_personnel>", methods=["GET"])
@admin_login_required
def api_desarchiver_personnel(id_personnel):
    """
    Désarchiver un personnel à partir de son id
    """
    return {"valide": archiver_personnel(id_personnel, archiver=False)}
