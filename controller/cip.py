from flask import Blueprint, render_template

from custom_paquets.decorateur import cip_login_required
from model.trace import get_commentaires_par_fiche
from model.apprenti import get_apprenti_by_login, get_id_apprenti_by_login
from model.ficheintervention import get_fiches_techniques_finies_par_login

cip = Blueprint("cip", __name__, url_prefix="/cip")

'''
Blueprint pour toutes les routes relatives aux URL des pages du CIP

Préfixe d'URL : /cip/ .
'''


@cip.route("/<apprenti>/choix-operations", methods=["GET"])
@cip_login_required
def affiche_choix(apprenti):
    """
    Page par défaut de la CIP. Une fois authentifiée, la CIP choisit l'action qu'elle souhaite effectuer
    (visualiser les fiches techniques, suivi de progression ou adaptation aux situations d'examen)

    :return: rendu de la page choix_operations.html
    """
    return render_template("cip/choix_operations.html", apprenti=apprenti)


@cip.route("/<apprenti>/fiches", methods=["GET"])
@cip_login_required
def fiches_apprenti(apprenti):
    """
    Récupère toutes les fiches techniques de l'élève sélectionné et les affiche.

    Permet de consulter les commentaires laissés par les éducateurs et l'élève en question. 

    :return: rendu de la page fiches_techniques.html
    """
    apprenti_infos = get_apprenti_by_login(apprenti)
    fiches = get_fiches_techniques_finies_par_login(apprenti)
    return render_template("cip/fiches_techniques.html", apprenti=apprenti_infos, fiches=fiches)


@cip.route("/<apprenti>/<fiche>/commentaires", methods=["GET"])
@cip_login_required
def visualiser_commentaires(apprenti, fiche):
    """
    Page de visualisation des commentaires de la CIP.
    En fonction de l'identifiant de l'élève et de la fiche sélectionnés, affiche les commentaires 
    des éducateurs et de l'apprenti. 
    
    :return: rendu de la page commentaires.html
    """

    commentaires = get_commentaires_par_fiche(fiche)
    return render_template("cip/commentaires.html", commentaires=commentaires), 200


@cip.route("/<apprenti>/suivi-progression", methods=["GET"])
@cip_login_required
def suivi_progression_apprenti(apprenti):
    """
    Page de suivi de progression de l'apprenti sélectionné. 
    Pour le moment ne fait que valider que l'on consulte le suivi de progression de l'apprenti sélectionné.
    
    :return: rendu de la page suivi-progression.html ?
    """
    return render_template("cip/suivi_progression_apprenti.html"), 200


@cip.route("/<apprenti>/adaptation-situation-examen", methods=["GET"])
@cip_login_required
def adaptation_situation_examen(apprenti):
    """
    Page de suivi d'adaptation en situation d'examen de l'apprenti sélectionné. 
    Pour le moment ne fait que valider que l'on consulte l'adaptation en situation d'examen
    de l'apprenti sélectionné.
    
    :return: rendu de la page adaptation-situation-examen.html ?
    """
    return "Adaptation en situation d'examen de " + apprenti
