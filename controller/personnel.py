from flask import Blueprint

personnel = Blueprint('personnel', __name__, url_prefix="/personnel")


@personnel.route("/redirection-connexion", methods=["GET"])
def redirection_connexion():
    return "connexion validée"
