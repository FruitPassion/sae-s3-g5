import urllib.parse

from flask import Blueprint, jsonify

from custom_paquets.decorateur import admin_login_required
from model.apprenti import check_password_apprenti, get_nbr_essaie_connexion_apprenti, archiver_apprenti
from model.formation import archiver_formation
from model.personnel import archiver_personnel

api = Blueprint('api', __name__, url_prefix="/api")


'''
Blueprint pour toutes les routes relatives aux URL d'API

Préfixe d'URL : /api/ .
'''


@api.route("/check-password-apprenti/<user>/<password>", methods=["GET", "POST"])
def api_check_password_apprenti(user, password):
    """
    Vérifie que le login et le password correspondent bien à ceux de la base de données
    """
    essaies = get_nbr_essaie_connexion_apprenti(user)
    if essaies != 5:
        return {"valide": check_password_apprenti(user, password)}, 200
    else:
        return {"blocage": True}, 200


@api.route("/archiver-formation/<id_formation>", methods=["GET", "POST"])
@admin_login_required
def api_archiver_formation(id_formation):
    """
    Archiver une formation à partir de son id
    """
    return jsonify({"valide": archiver_formation(id_formation)})


@api.route("/desarchiver-formation/<id_formation>", methods=["GET", "POST"])
@admin_login_required
def api_desarchiver_formation(id_formation):
    """
    Désarchiver une formation à partir de son id
    """
    return jsonify({"valide": archiver_formation(id_formation, archiver=False)})


@api.route("/archiver-apprenti/<id_apprenti>", methods=["GET", "POST"])
@admin_login_required
def api_archiver_apprenti(id_apprenti):
    """
    Archiver un apprenti à partir de son id
    """
    return jsonify({"valide": archiver_apprenti(id_apprenti)})


@api.route("/desarchiver-apprenti/<id_apprenti>", methods=["GET", "POST"])
@admin_login_required
def api_desarchiver_apprenti(id_apprenti):
    """
    Désarchiver un apprenti à partir de son id
    """
    return jsonify({"valide": archiver_apprenti(id_apprenti, archiver=False)})


@api.route("/archiver-personnel/<id_personnel>", methods=["GET", "POST"])
@admin_login_required
def api_archiver_personnel(id_personnel):
    """
    Archiver un personnel à partir de son id
    """
    return jsonify({"valide": archiver_personnel(id_personnel)})


@api.route("/desarchiver-personnel/<id_personnel>", methods=["GET", "POST"])
@admin_login_required
def api_desarchiver_personnel(id_personnel):
    """
    Désarchiver un personnel à partir de son id
    """
    return jsonify({"valide": archiver_personnel(id_personnel, archiver=False)})