from flask import Blueprint, render_template

from custom_paquets.decorateur import admin_login_required

admin = Blueprint("admin", __name__, url_prefix="/admin")


'''
Blueprint pour toutes les routes relatives aux pages super admin.

Préfixe d'URL : /admin/ .
'''


@admin.route("/accueil-admin", methods=["GET"])
@admin_login_required
def accueil_admin():
    return render_template("admin/accueil_superadmin.html")
