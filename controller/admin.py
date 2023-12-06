import os
import platform

from PIL import Image
from unidecode import unidecode

from flask import Blueprint, redirect, render_template, request, url_for

from custom_paquets.decorateur import admin_login_required
from custom_paquets.gestion_image import resize_image
from model.apprenti import get_all_apprenti, add_apprenti
from model.personnel import get_all_personnel
from model.formation import get_all_formation
from model.session import get_all_sessions, add_apprenti_assister
from custom_paquets.custom_form import AjouterApprenti
from werkzeug.utils import secure_filename

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


@admin.route("/gestion-apprenti", methods=["GET", "POST"])
@admin_login_required
def gestion_apprenti():
    """
    Page listant tous les comptes des apprentis et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter du personnel
    """

    formations = get_all_formation()
    apprenti = get_all_apprenti()
    form = AjouterApprenti()
    if form.validate_on_submit() and request.method == "POST":
        login = unidecode(form.nom.data[0:2].upper().strip()) + unidecode(form.prenom.data[0].upper().strip()) + str(
            len(form.nom.data.strip() + form.prenom.data.strip())).zfill(2)
        f = request.files.get("avatar")
        if f:
            chemin_avatar = "./static/images/photo_profile/" + secure_filename(f.filename)
            f.save(chemin_avatar)
            chemin_avatar = "photo_profile/" + secure_filename(f.filename)
        else:
            chemin_avatar = "photo_profile/" + "default_profile.png"
        img = Image.open(f.stream)
        resize_image(img, "./static/images/"+chemin_avatar)
        id_apprenti = add_apprenti(form.nom.data, form.prenom.data, login, chemin_avatar)
        add_apprenti_assister(id_apprenti, formations[int(request.form.get("select_formation")) - 1]["id_formation"])
        return redirect(url_for("admin.gestion_apprenti"))

    return render_template("admin/gestion_apprentis.html", liste_apprenti=apprenti, form=form, formations=formations)


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
