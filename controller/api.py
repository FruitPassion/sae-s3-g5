import urllib.parse

from flask import Blueprint, jsonify
from custom_paquets.security import passwordStrenght

api = Blueprint('api', __name__, url_prefix="/api")


@api.route("/password-strengh/<password>", methods=["GET"])
def api_password_strenght(password):
    return jsonify(passwordStrenght(urllib.parse.unquote(password)))
