from flask import Blueprint, render_template
from model.formation import getAllFormation
from model.assister import getApprentisByFormation

personnel = Blueprint("personnel", __name__, url_prefix="/personnel")


'''
Blueprint pour toutes les routes relatives aux URL des pages du personnel (non super admin)

Préfixe d'URL : /personnel/ .
'''


@personnel.route("/redirection-connexion", methods=["GET"])
def redirection_connexion():
    formations = getAllFormation()
    return render_template("personnel/choix_formation.html", formations = formations)

@personnel.route("/choix-eleves/<nom_formation>", methods =["GET"])
def choix_eleve(nom_formation):
    apprentis = getApprentisByFormation(nom_formation)
    return render_template("personnel/choix_apprentis.html", apprentis = apprentis)

@personnel.route("/personnalisation", methods=["GET"])
def personnalisation():
    liste_police = ["Arial","Courier New", "Times New Roman", "Verdana", "Impact", "Montserrat", "Roboto", "Open Sans", "Lato", "Oswald", "Poppins"]

    return render_template('personnel/personnaliser_fiche_texte_champs.html', polices=liste_police)


@personnel.route("/personnalisation-bis", methods=["GET"])
def personnalisation_bis():
    return render_template('personnel/personnaliser_fiche_couleur_fond.html')
