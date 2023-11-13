from flask import Blueprint, render_template
from model.cip import getCommentairesParLoginEleve

cip = Blueprint("cip", __name__, url_prefix="/cip")


'''
Blueprint pour toutes les routes relatives aux URL des pages du CIP

Préfixe d'URL : /cip/ .
'''

@cip.route("/choix-formation/choix-apprenti/choix-action/fiches-techniques/visualisation-commentaires.html", methods=["GET"]):
def afficher_commentaires(login : str):
    commentaires = getCommentairesParLoginEleve(login)
    return render_template("cip/afficher_commentaires.html", commentaires = commentaires)