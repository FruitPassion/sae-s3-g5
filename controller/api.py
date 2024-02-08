import urllib.parse, uuid, os

from flask import Blueprint, jsonify, request

from custom_paquets.decorateur import admin_login_required, personnel_login_required
from model.apprenti import Apprenti
from model.formation import Formation
from model.personnel import Personnel
from model.cours import Cours
from model.trace import Trace

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
    if Apprenti.get_nbr_essais_connexion_apprenti(user) != 5:
        return {"valide": Apprenti.check_password_apprenti(user, password)}
    else:
        return {"blocage": True}


@api.route("/set-password-apprenti/<user>/<password>", methods=["GET"])
def api_set_password_apprenti(user, password):
    """
    Modifie le mot de passe d'un apprenti

    :param user: Login de l'apprenti
    :param password: Nouveau mot de passe
    """
    if Apprenti.check_password_apprenti(user, password):
        return {"valide": False}
    else:
        return {"valide": Apprenti.set_password_apprenti(user, password)}


@api.route("/archiver-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_archiver_formation(id_formation, commit=True):
    """
    Archive une formation à partir de son id
    """
    return {"valide": Formation.archiver_formation(id_formation, commit=commit), "retirer": True}


@api.route("/reinitialiser-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_reinitialiser_formation(id_formation, commit=True):
    """
    Réinitialise une formation à partir de son id

    :param id_formation:
    :param commit:
    :return: JSON valide
    """
    return {"valide": Formation.reinitisaliser_formation(id_formation, commit=commit)}


@api.route("/desarchiver-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_desarchiver_formation(id_formation):
    """
    Désarchive une formation à partir de son id

    :param id_formation:
    :return: JSON valide
    """
    return {"valide": Formation.archiver_formation(id_formation, archiver=False)}


@api.route("/supprimer-formation/<id_formation>", methods=["GET"])
@admin_login_required
def api_supprimer_formation(id_formation):
    """
    Supprime une formation à partir de son id
    """
    return {"valide": Formation.remove_formation(id_formation)}


@api.route("/archiver-apprenti/<id_apprenti>", methods=["GET"])
@admin_login_required
def api_archiver_apprenti(id_apprenti):
    """
    Archive un apprenti à partir de son id
    """
    return {"valide": Apprenti.archiver_apprenti(id_apprenti), "retirer": True}


@api.route("/desarchiver-apprenti/<id_apprenti>", methods=["GET"])
@admin_login_required
def api_desarchiver_apprenti(id_apprenti):
    """
    Désarchive un apprenti à partir de son id
    """
    return {"valide": Apprenti.archiver_apprenti(id_apprenti, archiver=False)}


@api.route("/supprimer-apprenti/<id_apprenti>", methods=["GET"])
@admin_login_required
def api_supprimer_apprenti(id_apprenti):
    """
    Supprime un apprenti à partir de son id
    """
    return {"valide": Apprenti.remove_apprenti(id_apprenti)}


@api.route("/archiver-cours/<id_cours>", methods=["GET"])
@admin_login_required
def api_archiver_cours(id_cours):
    """
    Archive un cours à partir de son id
    """
    return {"valide":Cours.archiver_cours(id_cours), "retirer": True}


@api.route("/desarchiver-cours/<id_cours>", methods=["GET"])
@admin_login_required
def api_desarchiver_cours(id_cours):
    """
    Désarchive un cours à partir de son id
    """
    return {"valide": Cours.archiver_cours(id_cours, archiver=False)}


@api.route("/supprimer-cours/<id_cours>", methods=["GET"])
@admin_login_required
def api_supprimer_cours(id_cours):
    """
    Supprime un cours à partir de son id
    """
    return {"valide": Cours.remove_cours(id_cours)}


@api.route("/archiver-personnel/<id_personnel>", methods=["GET"])
@admin_login_required
def api_archiver_personnel(id_personnel):
    """
    Archive un personnel à partir de son id
    """
    return {"valide": Personnel.archiver_personnel(id_personnel), "retirer": True}


@api.route("/desarchiver-personnel/<id_personnel>", methods=["GET"])
@admin_login_required
def api_desarchiver_personnel(id_personnel):
    """
    Désarchive un personnel à partir de son id
    """
    return {"valide": Personnel.archiver_personnel(id_personnel, archiver=False)}


@api.route("/supprimer-personnel/<id_personnel>", methods=["GET"])
@admin_login_required
def api_supprimer_personnel(id_personnel):
    """
    Supprime un personnel à partir de son id
    """
    return {"valide": Personnel.remove_personnel(id_personnel)}


@api.route("/save_audio/<id_personnel>", methods=['POST'])
@personnel_login_required
def save_audio(id_personnel, id_fiche, horodatage, commentaire_audio):
    if 'commentaire_audio' in request.files:
        audio_file = request.files['commentaire_audio']
        if audio_file.filename != '':
            filename = f"{id_fiche}.{id_personnel}.mp3"
            commentaire_audio = os.path.join('static/audio', filename)
            audio_file.save(commentaire_audio)

    return {"valide": Trace.modifier_commentaire_audio(id_fiche, horodatage, commentaire_audio)}
