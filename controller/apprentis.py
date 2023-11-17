from flask import Blueprint, render_template
from custom_paquets.decorateur import apprenti_login_required

apprenti = Blueprint('apprenti', __name__, url_prefix="/apprenti")


'''
Blueprint pour toutes les routes relatives aux URL des pages d'apprentis

Préfixe d'URL : /apprenti/ .
'''


@apprenti.route("/redirection-connexion", methods=["GET"])
@apprenti_login_required
def redirection_connexion():
    return render_template("apprentis/accueil_apprentis.html")

