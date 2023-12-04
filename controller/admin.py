from flask import Blueprint, render_template

from custom_paquets.decorateur import admin_login_required
from model.apprenti import get_all_apprenti
from model.personnel import get_all_personnel
from model.formation import get_all_formation
from model.session import get_all_sessions

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
    """
    return render_template("admin/accueil_superadmin.html")


@admin.route("/gestion-personnel", methods=["GET"])
@admin_login_required
def gestion_personnel():
    """
    Page listant tous les comptes du personnel et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter du personnel
    """
    couleurs = {"SuperAdministrateur": "text-primary", "Educateur Administrateur": "text-warning",
                "Educateur": "text-success", "CIP": "text-info"}
    personnel = get_all_personnel()
    return render_template("admin/gestion_personnel.html", liste_personnel=personnel, couleurs=couleurs)


@admin.route("/gestion-apprenti", methods=["GET"])
@admin_login_required
def gestion_apprenti():
    """
    Page listant tous les comptes des apprentis et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter du personnel
    """
    apprenti = get_all_apprenti()
    return render_template("admin/gestion_apprentis.html", liste_apprenti=apprenti)


@admin.route("/gestion-formation", methods=["GET"])
@admin_login_required
def gestion_formation():
    """
    Page listant toutes les formations et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter une formation
    """
    formation = get_all_formation()
    return render_template("admin/gestion_formations.html", liste_formation=formation)


@admin.route("/gestion-session", methods=["GET"])
@admin_login_required
def gestion_session():
    """
    Page listant toutes les formations et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter une formation
    """
    sessions = get_all_sessions()
    return render_template("admin/gestion_sessions.html", liste_sessions=sessions)