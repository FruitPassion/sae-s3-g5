from flask import Blueprint, render_template

from custom_paquets.decorateur import personnel_login_required
educ_admin = Blueprint("cip", __name__, url_prefix="/educ-admin")


'''
Blueprint pour toutes les routes relatives aux URL des pages des educs admin

Préfixe d'URL : /educ-admin/ .
'''
# ALED Raphael :')
@educ_admin.route("/choix-eleves/<formation>/<apprenti>/fiches-apprenti", methods=["GET"])
@personnel_login_required
def fiches_apprenti(apprenti):
    fiches = [] # récupérer les fiches de l'apprenti mais bon, à voir par rapport aux requêtes
    return render_template("personnel/choix_fiches_apprenti.html", fiches, apprenti=apprenti)