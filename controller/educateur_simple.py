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
    """
    Page par défaut de l'éducateur simple.
    Ce dernier ne peut que commenter une fiche technique d'un apprenti.
    
    Pour le moment, ne fait que valider que la connexion en tant qu'éducateur simple fonctionne et qu'il
    consulte les fiches de l'élève sélectionné.
    
    :return: les fiches techniques de l'élève sélectionné.
    """
    return "Connecté en tant que educ simple \n voici les fiches de " + apprenti
