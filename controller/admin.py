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
    """
    Page vers laquelle est redirigé le superadmin une fois authentifié.
    Aura ensuite accès à une page lui permettant de choisir une action (gérer les comptes, les formations ou les élèves )

    :return: rendu de la page accueil_superadmin.html
    """
    return render_template("admin/accueil_superadmin.html")
