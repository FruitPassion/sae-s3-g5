from flask import Blueprint, render_template

from custom_paquets.decorateur import cip_login_required
from model.cip import get_commentaires_par_login_eleve

cip = Blueprint("cip", __name__, url_prefix="/cip")


'''
Blueprint pour toutes les routes relatives aux URL des pages du CIP

Préfixe d'URL : /cip/ .
'''


@cip.route("/<apprenti>/<id_fiche>/visualisation-commentaires", methods=["GET"])
@cip_login_required
def afficher_commentaires(apprenti, id_fiche):
    commentaires = get_commentaires_par_login_eleve(apprenti)
    return render_template("cip/afficher_commentaires.html", commentaires = commentaires, id_fiche = id_fiche)


@cip.route("/<apprenti>/choix-operations", methods=["GET"])
@cip_login_required
def affiche_choix(apprenti):
    return render_template("cip/choix_operations.html", apprenti=apprenti);


@cip.route("/<apprenti>/fiches", methods=["GET"])
@cip_login_required
def fiches_apprenti(apprenti):
    return "Voici les fiches de " + apprenti


@cip.route("/<apprenti>/suivi-progression", methods=["GET"])
@cip_login_required
def suivi_progression_apprenti(apprenti):
    return "Suivi de progression de " + apprenti


@cip.route("/<apprenti>/adaptation-situation-examen", methods=["GET"])
@cip_login_required
def adaptation_situation_examen(apprenti):
    return "Adaptation en situation d'examen de " + apprenti
