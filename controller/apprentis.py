from flask import Blueprint, render_template, session
from custom_paquets.decorateur import apprenti_login_required
from model.apprenti import get_apprenti_by_login
from model.ficheintervention import get_etat_fiche_par_id_fiche, get_fiches_techniques_par_login

apprenti = Blueprint('apprenti', __name__, url_prefix="/apprenti")


'''
Blueprint pour toutes les routes relatives aux URL des pages d'apprentis

Préfixe d'URL : /apprenti/ .
'''


@apprenti.route("/redirection-connexion", methods=["GET"])
@apprenti_login_required
def redirection_connexion():
    """
    Page de redirection des apprentis une fois qu'ils sont authentifiés.
    Ils accèdent à la liste de leurs fiches techniques.

    :return: rendu de la page accueil_apprentis.html
    """
    apprenti_infos = get_apprenti_by_login(session["name"])
    fiches = get_fiches_techniques_par_login(session['name'])
    return render_template("apprentis/accueil_apprentis.html", fiches=fiches, apprenti=apprenti_infos)


@apprenti.route("/redirection-connexion/suivi", methods=["GET"])
@apprenti_login_required
def suivi_progression():
    """
    Page de suivi de progression des apprentis
    
    :return: rendu de la page suivi_progression_apprenti.html
    """
    fiches_apprenti = get_fiches_techniques_par_login(session['name'])
    etat_fiches = {}
    for fiche in fiches_apprenti:
        etat_fiches[fiche["id_fiche"]] = get_etat_fiche_par_id_fiche(fiche["id_fiche"])
    return render_template("apprentis/suivi_progression_apprenti.html", etat_fiches=etat_fiches)