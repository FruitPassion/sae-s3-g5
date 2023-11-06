from flask import Blueprint, render_template

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/redirection-connexion", methods=["GET"])
def redirection_connexion():
    return render_template("admin/accueil_superadmin.html")
