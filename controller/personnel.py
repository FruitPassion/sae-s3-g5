from flask import Blueprint, render_template

personnel = Blueprint("personnel", __name__, url_prefix="/personnel")


@personnel.route("/redirection-connexion", methods=["GET"])
def redirection_connexion():
    return render_template("personnel/choix_formation.html")


@personnel.route("/personnalisation", methods=["GET"])
def personnalisation():
    liste_police = ["Arial","Courier New", "Times New Roman", "Verdana", "Impact", "Montserrat", "Roboto", "Open Sans", "Lato", "Oswald", "Poppins"]

    return render_template('personnel/personnaliser_fiche_texte_champs.html', polices=liste_police)


@personnel.route("/personnalisation-bis", methods=["GET"])
def personnalisation_bis():
    return render_template('personnel/personnaliser_fiche_couleur_fond.html')
