from flask import Blueprint, render_template, session
from custom_paquets.decorateur import apprenti_login_required
from model.apprenti import get_apprenti_by_login
from model.ficheintervention import get_fiches_techniques_par_login

apprenti = Blueprint('apprenti', __name__, url_prefix="/apprenti")


'''
Blueprint pour toutes les routes relatives aux URL des pages d'apprentis

Préfixe d'URL : /apprenti/ .
'''


@apprenti.route("/redirection-connexion", methods=["GET"])
@apprenti_login_required
def redirection_connexion():
    apprenti_infos = get_apprenti_by_login(session["name"])
    fiches = get_fiches_techniques_par_login(session['name'])
    return render_template("apprentis/accueil_apprentis.html", fiches=fiches, apprenti=apprenti_infos[0])

