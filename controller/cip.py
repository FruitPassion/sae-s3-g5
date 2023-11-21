from flask import Blueprint, render_template

from custom_paquets.decorateur import cip_login_required
from model.cip import get_commentaires_par_login_eleve
from model.apprenti import get_apprenti_by_login
from model.ficheintervention import get_fiches_techniques_par_login

cip = Blueprint("cip", __name__, url_prefix="/cip")

'''
Blueprint pour toutes les routes relatives aux URL des pages du CIP

Préfixe d'URL : /cip/ .
'''


@cip.route("/<apprenti>/choix-operations", methods=["GET"])
@cip_login_required
def affiche_choix(apprenti):
    return render_template("cip/choix_operations.html", apprenti=apprenti)


@cip.route("/<apprenti>/fiches", methods=["GET"])
@cip_login_required
def fiches_apprenti(apprenti):
    apprenti_infos = get_apprenti_by_login(apprenti)
    fiches = get_fiches_techniques_par_login(apprenti)
    return render_template("cip/fiches_techniques.html", apprenti=apprenti_infos[0], fiches=fiches)


@cip.route("/<apprenti>/<fiche>/commentaires", methods=["GET"])
@cip_login_required
def visualiser_commentaires(apprenti, fiche):
    commentaires = get_commentaires_par_login_eleve(apprenti, fiche)
    return render_template("cip/commentaires.html", commentaires=commentaires)


@cip.route("/<apprenti>/suivi-progression", methods=["GET"])
@cip_login_required
def suivi_progression_apprenti(apprenti):
    return "Suivi de progression de " + apprenti


@cip.route("/<apprenti>/adaptation-situation-examen", methods=["GET"])
@cip_login_required
def adaptation_situation_examen(apprenti):
    return "Adaptation en situation d'examen de " + apprenti
