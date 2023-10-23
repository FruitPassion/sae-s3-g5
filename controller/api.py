import urllib.parse

from flask import Blueprint, jsonify
from custom_paquets.security import passwordStrenght
from model.apprenti import checkPasswordApprenti

api = Blueprint('api', __name__, url_prefix="/api")


@api.route("/check-password-apprenti/<user>/<password>", methods=["GET", "POST"])
def api_check_password_apprenti(user, password):
    return {"valide": checkPasswordApprenti(user, password)}
