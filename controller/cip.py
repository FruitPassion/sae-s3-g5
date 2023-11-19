from flask import Blueprint, render_template

from custom_paquets.decorateur import cip_login_required
from model.cip import get_commentaires_par_login_eleve

cip = Blueprint("cip", __name__, url_prefix="/cip")


'''
Blueprint pour toutes les routes relatives aux URL des pages du CIP

Préfixe d'URL : /cip/ .
'''


@cip.route("/<formation>/<apprenti>/<id_fiche>/visualisation-commentaires", methods=["GET"])
@cip_login_required
def afficher_commentaires(formation, apprenti, id_fiche):
    commentaires = get_commentaires_par_login_eleve(apprenti)
    return render_template("cip/afficher_commentaires.html", commentaires = commentaires)


@cip.route("/<apprenti>/fiches", methods=["GET"])
@cip_login_required
def fiches_apprenti(apprenti):
    return "Connecté en tant que cip \n voici les fiches de " + apprenti
