from flask import Blueprint, render_template

from custom_paquets.decorateur import personnel_login_required

educ_admin = Blueprint("educ_admin", __name__, url_prefix="/educ-admin")

'''
Blueprint pour toutes les routes relatives aux URL des pages des educs admin

Préfixe d'URL : /educ-admin/ .
'''


# ALED Raphael :')
@educ_admin.route("/<apprenti>/fiches", methods=["GET"])
@personnel_login_required
def fiches_apprenti(apprenti):
    fiches = []
    return "Connecté en tant que educ admin \n voici les fiches de " + apprenti
    # return render_template("personnel/choix_fiches_apprenti.html", apprenti=apprenti)
