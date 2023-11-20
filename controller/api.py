import urllib.parse

from flask import Blueprint, jsonify
from model.apprenti import check_password_apprenti

api = Blueprint('api', __name__, url_prefix="/api")


'''
Blueprint pour toutes les routes relatives aux URL d'API

Préfixe d'URL : /api/ .
'''


@api.route("/check-password-apprenti/<user>/<password>", methods=["GET", "POST"])
def api_check_password_apprenti(user, password):
    return {"valide": check_password_apprenti(user, password)}, 200
