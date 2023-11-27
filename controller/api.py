import urllib.parse

from flask import Blueprint, jsonify
from model.apprenti import check_password_apprenti, get_nbr_essaie_connexion_apprenti

api = Blueprint('api', __name__, url_prefix="/api")


'''
Blueprint pour toutes les routes relatives aux URL d'API

Préfixe d'URL : /api/ .
'''


@api.route("/check-password-apprenti/<user>/<password>", methods=["GET", "POST"])
def api_check_password_apprenti(user, password):
    """
    Vérifie que le login et le password correspondent bien à ceux de la base de données
    """
    essaies = get_nbr_essaie_connexion_apprenti(user)
    if essaies != 5:
        return {"valide": check_password_apprenti(user, password)}, 200
    else:
        return {"blocage": True}, 200
