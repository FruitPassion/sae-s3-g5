from custom_paquets.converter import generate_login
from custom_paquets.security import encrypt_password

from flask import Blueprint, Response, redirect, render_template, request, url_for

from custom_paquets.decorateur import admin_login_required
from custom_paquets.gestion_image import stocker_photo_profile, supprimer_photo_profil
from custom_paquets.gestion_image import stocker_image_formation
from model.apprenti import Apprenti
from model.personnel import Personnel
from model.formation import Formation
from model.cours import Cours
from custom_paquets.custom_form import AjouterApprenti, ModifierApprenti, ModifierPersonnel, ModifierAdmin
from custom_paquets.custom_form import AjouterPersonnel
from custom_paquets.custom_form import AjouterFormation, ModifierFormation

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


@admin.route("/gestion-personnel", methods=["GET", "POST"])
@admin_login_required
def gestion_personnel():
    """
    Page listant tous les comptes du personnel et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter du personnel
    """
    couleurs = {"SuperAdministrateur": "text-primary", "Educateur Administrateur": "text-warning",
                "Educateur": "text-success", "CIP": "text-info"}
    personnel = Personnel.get_all_personnel()
    liste_personnel_archive = Personnel.get_all_personnel(archive=True)
    form_ajouter = AjouterPersonnel()
    form_modifier = ModifierPersonnel()
    form_modifier_admin = ModifierAdmin()
    REDIRECTION = "admin.gestion_personnel"

    if (form_modifier_admin.validate_on_submit() and form_modifier.validate_on_submit() and 'Modifier Admin'
            in request.form.values()):
        role = "SuperAdministrateur"
        identifiant = request.form.get("id-element")
        login = generate_login(form_modifier.form_nom.data, form_modifier.form_prenom.data)
        if form_modifier_admin.form_password.data:
            new_password = encrypt_password(form_modifier_admin.form_password.data)
        else:
            new_password = None
        Personnel.update_personnel(identifiant, login, form_modifier_admin.form_nom.data,
                         form_modifier_admin.form_prenom.data, form_modifier_admin.form_email.data,
                         role, password=new_password)
        return redirect(url_for(REDIRECTION), 302)

    elif form_modifier.validate_on_submit() and request.method == "POST" and 'Modifier' in request.form.values():
        nouveau_role = request.form.get("nouveau_role").replace("_", " ")
        identifiant = request.form.get("id-element")
        login = generate_login(form_modifier.form_nom.data, form_modifier.form_prenom.data)

        if form_modifier.form_password.data:
            new_password = encrypt_password(form_modifier.form_password.data)
        else:
            new_password = None
        actif = request.form.get("form_actif") == "on"
        Personnel.update_personnel(identifiant, login, form_modifier.form_nom.data, form_modifier.form_prenom.data,
                         form_modifier.form_email.data, nouveau_role, actif=actif, password=new_password)
        return redirect(url_for(REDIRECTION), 302)

    elif form_ajouter.validate_on_submit() and request.method == "POST":
        role = request.form.get("select_role")
        password = encrypt_password(request.form.get('password'))
        login = generate_login(form_ajouter.nom.data, form_ajouter.prenom.data)
        Personnel.add_personnel(login, form_ajouter.nom.data, form_ajouter.prenom.data, form_ajouter.email.data, password, role)
        return redirect(url_for(REDIRECTION), 302)

    return Response(render_template("admin/gestion_personnel.html", liste_personnel=personnel,
                           form_ajouter=form_ajouter, form_modifier=form_modifier,
                           form_modifier_admin=form_modifier_admin, couleurs=couleurs,
                           liste_personnel_archive=liste_personnel_archive), 200)


@admin.route("/gestion-apprentis", methods=["GET", "POST"])
@admin_login_required
def gestion_apprentis():
    """
    Page listant tous les comptes des apprentis et permettant de supprimer, modifier, archiver et désarchiver leur
    compte.
    On peux également ajouter des apprentis.
    """

    formations = Formation.get_all_formations()
    apprentis = Apprenti.get_all_apprentis()
    liste_apprentis_archives = Apprenti().get_all_apprentis(archive=True)
    form_ajouter = AjouterApprenti()
    form_modifier = ModifierApprenti()
    if form_modifier.validate_on_submit() and request.method == "POST":
        identifiant = request.form.get("id-element")
        chemin_ancien_avatar = Apprenti.get_photos_profil_apprenti(identifiant)
        login = generate_login(form_modifier.form_nom.data, form_modifier.form_prenom.data)
        if len(request.files.get("avatar-modifier").filename) != 0:
            if chemin_ancien_avatar != "photo_profile/defaut_profile.png":
                supprimer_photo_profil(chemin_ancien_avatar)
            f = request.files.get("avatar-modifier")
            chemin_avatar = stocker_photo_profile(f)
        else:
            chemin_avatar = Apprenti.get_photos_profil_apprenti(identifiant)
        actif = (request.form.get("form_actif") == "on")
        reinitialiser_pass = (request.form.get("form_reinitialiser") == "on")
        Apprenti.update_apprenti(identifiant, login, form_modifier.form_nom.data, form_modifier.form_prenom.data, chemin_avatar,
                        reinitialiser_pass, actif)
        return redirect(url_for("admin.gestion_apprentis"), 302)
    elif form_ajouter.validate_on_submit() and request.method == "POST":
        login = generate_login(form_ajouter.nom.data, form_ajouter.prenom.data)
        f = request.files.get("avatar")
        chemin_avatar = stocker_photo_profile(f)
        id_apprenti = Apprenti.add_apprenti(form_ajouter.nom.data, form_ajouter.prenom.data, login, chemin_avatar)
        Cours.add_apprenti_assister(id_apprenti, formations[int(request.form.get("select_formation")) - 1].id_formation)
        return redirect(url_for("admin.gestion_apprentis"), 302)

    return Response(render_template("admin/gestion_apprentis.html", liste_apprentis=apprentis,
                           form_ajouter=form_ajouter, form_modifier=form_modifier, formations=formations,
                           liste_apprentis_archives=liste_apprentis_archives), 200)


@admin.route("/gestion-formations", methods=["GET", "POST", "DELETE"])
@admin_login_required
def gestion_formations():
    """
    Page listant toutes les formations et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter une formation
    """
    formations = Formation.get_all_formations()
    liste_formations_archivees = Formation.get_all_formations(archive=True)
    form = AjouterFormation()
    form_modifier = ModifierFormation()
    if form.validate_on_submit() and request.method == "POST":
        f = request.files.get("image")
        if f:
            chemin_image = stocker_image_formation(f)
        else:
            chemin_image = "formation_image/default_formation.png"
        Formation.add_formation(form.intitule.data, form.niveau_qualif.data, form.groupe.data, chemin_image)
        return redirect(url_for("admin.gestion_formations"), 302)

    elif form_modifier.validate_on_submit() and request.method == "POST":
        identifiant = request.form.get("id-element")
        if len(request.files.get("image-formation").filename) != 0:
            f = request.files.get("image-formation")
            chemin_image = stocker_image_formation(f)
        else:
            chemin_image = Formation.get_image_formation(identifiant)
        Formation.update_formation(identifiant, form_modifier.form_intitule.data, form_modifier.form_niveau_qualif.data,
                         form_modifier.form_groupe.data, chemin_image)
        return redirect(url_for("admin.gestion_formations"), 302)

    return Response(render_template("admin/gestion_formations.html", liste_formations=formations, form=form,
                           form_modifier=form_modifier, liste_formations_archivees=liste_formations_archivees), 200)
