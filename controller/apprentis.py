from flask import Blueprint, render_template

apprenti = Blueprint('apprenti', __name__, url_prefix="/apprenti")


@apprenti.route("/redirection-connexion", methods=["GET"])
def redirection_connexion():
    return render_template("apprentis/accueil_apprentis.html")

