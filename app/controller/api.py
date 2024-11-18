from flask import Blueprint, request

from custom_paquets.decorateur import admin_login_required
from model.apprenti import Apprenti
from model.cours import Cours
from model.formation import Formation
from model.personnel import Personnel

api = Blueprint("api", __name__, url_prefix="/api")

"""
Blueprint pour toutes les routes relatives aux URL d'API

Préfixe d'URL : /api/ .
"""


@api.route("/check-password-apprenti/", methods=["POST"])
def api_check_password_apprenti():
    """
    Vérifie que le login et le password correspondent bien à ceux de la base de données
    """
    infos = request.get_json()

    if Apprenti.get_nbr_essais_connexion_apprenti(infos["login"]) != 5:
        return {"valide": Apprenti.check_password_apprenti(infos["login"], infos["password"])}
    else:
        return {"blocage": True}


@api.route("/set-password-apprenti/", methods=["POST"])
def api_set_password_apprenti():
    """
    Modifie le mot de passe d'un apprenti

    :param user: Login de l'apprenti
    :param password: Nouveau mot de passe
    """
    infos = request.get_json()

    if not Apprenti.check_apprenti(infos["login"]) or not Apprenti.check_password_non_set(infos["login"]):
        return {"valide": False}
    else:
        return {"valide": Apprenti.set_password_apprenti(infos["login"], str(infos["password"]))}


@api.route("/reinitialiser-formation/<int:id_formation>", methods=["PATCH"])
@admin_login_required
def api_reinitialiser_formation(id_formation):
    """
    Réinitialise une formation à partir de son id

    :param id_formation:
    :param commit:
    :return: JSON valide
    """
    return {"valide": Formation.reinitisaliser_formation(id_formation)}


@api.route("/formation/<int:id_formation>", methods=["PATCH"])
@admin_login_required
def api_archive_formation(id_formation):
    """
    Désarchive une formation à partir de son id

    :param id_formation:
    :return: JSON valide
    """
    infos = request.get_json()
    return {"valide": Formation.archiver_formation(id_formation, archiver=infos["archive"])}


@api.route("/formation/<int:id_formation>", methods=["DELETE"])
@admin_login_required
def api_supprimer_formation(id_formation):
    """
    Supprime une formation à partir de son id
    """
    return {"valide": Formation.remove_formation(id_formation)}


@api.route("/apprenti/<int:id_apprenti>", methods=["PATCH"])
@admin_login_required
def api_archive_apprenti(id_apprenti):
    """
    Archive/Désarchive un apprenti à partir de son id
    """
    infos = request.get_json()
    return {"valide": Apprenti.archiver_apprenti(id_apprenti, archiver=infos["archive"])}


@api.route("/apprenti/<int:id_apprenti>", methods=["DELETE"])
@admin_login_required
def api_supprimer_apprenti(id_apprenti):
    """
    Supprime un apprenti à partir de son id
    """
    return {"valide": Apprenti.remove_apprenti(id_apprenti)}


@api.route("/cours/<int:id_cours>", methods=["PATCH"])
@admin_login_required
def api_archive_cours(id_cours):
    """
    Archive/Désarchive un cours à partir de son id
    """
    infos = request.get_json()
    return {"valide": Cours.archiver_cours(id_cours, archiver=infos["archive"])}


@api.route("/cours/<int:id_cours>", methods=["DELETE"])
@admin_login_required
def api_supprimer_cours(id_cours):
    """
    Supprime un cours à partir de son id
    """
    return {"valide": Cours.remove_cours(id_cours)}


@api.route("/personnel/<int:id_personnel>", methods=["PATCH"])
@admin_login_required
def api_archive_personnel(id_personnel):
    """
    Archive/Désarchive un personnel à partir de son id
    """
    infos = request.get_json()

    return {"valide": Personnel.archiver_personnel(id_personnel, archiver=infos["archive"])}


@api.route("/personnel/<int:id_personnel>", methods=["DELETE"])
@admin_login_required
def api_supprimer_personnel(id_personnel):
    """
    Supprime un personnel à partir de son id
    """
    return {"valide": Personnel.remove_personnel(id_personnel)}
