from flask import Blueprint, render_template

from custom_paquets.decorateur import educadmin_login_required

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
    return render_template("personnel/choix_fiches_apprenti.html", apprenti=apprenti)
