from flask import Blueprint, render_template

from custom_paquets.decorateur import educsimple_login_required

educ_simple = Blueprint("educ_simple", __name__, url_prefix="/educ-simple")


'''
Blueprint pour toutes les routes relatives aux URL des pages des éducateurs simples

Préfixe d'URL : /educ-simple/ .
'''


@educ_simple.route("/<apprenti>/fiches", methods=["GET"])
@educsimple_login_required
def fiches_apprenti(apprenti):
    return "Connecté en tant que educ simple \n voici les fiches de " + apprenti
