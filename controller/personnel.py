from flask import Blueprint, render_template

personnel = Blueprint("personnel", __name__, url_prefix="/personnel")


@personnel.route("/redirection-connexion", methods=["GET"])
def redirection_connexion():
    return render_template("personnel/accueil_superadmin.html")


@personnel.route("/personnalisation", methods=["GET"])
def personnalisation():
    liste_police = ["Arial","Courier New", "Times New Roman", "Verdana", "Impact", "Montserrat", "Roboto", "Open Sans", "Lato", "Oswald", "Poppins"]

    return render_template('personnel/personnaliser_fiche_texte_champs.html', polices=liste_police)
