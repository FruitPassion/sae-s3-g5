from flask import Blueprint, render_template

from custom_paquets.decorateur import educadmin_login_required
from model.apprenti import get_apprenti_by_login
from model.ficheintervention import get_fiches_techniques_finies_par_login

educ_admin = Blueprint("educ_admin", __name__, url_prefix="/educ-admin")

'''
Blueprint pour toutes les routes relatives aux URL des pages des educs admin

Préfixe d'URL : /educ-admin/ .
'''

@educ_admin.route("/<apprenti>/choix-operations", methods=["GET"])
@educadmin_login_required
def affiche_choix(apprenti):
    return render_template("personnel/choix_actions.html", apprenti=apprenti)


@educ_admin.route("/<apprenti>/fiches", methods=["GET"])
@educadmin_login_required
def fiches_apprenti(apprenti):
    """
    Récupère toutes les fiches techniques de l'élève sélectionné et les affiche.

    Permet de consulter les commentaires laissés par les éducateurs et l'élève en question. 

    :return: rendu de la page fiches_techniques.html
    """
    apprenti_infos = get_apprenti_by_login(apprenti)
    fiches = get_fiches_techniques_finies_par_login(apprenti)
    return render_template("personnel/choix_fiches_apprenti.html", apprenti=apprenti_infos, fiches=fiches)
