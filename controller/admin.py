from custom_paquets.converter import generate_login
from custom_paquets.security import encrypt_password

from flask import Blueprint, redirect, render_template, request, url_for

from custom_paquets.decorateur import admin_login_required
from custom_paquets.gestion_image import stocker_photo_profile
from model.apprenti import get_all_apprenti, add_apprenti, get_photo_profil_apprenti, update_apprenti
from model.personnel import get_all_personnel, add_personnel, update_personnel
from model.formation import get_all_formation, add_formation, update_formation, get_image_formation
from model.session import add_apprenti_assister
from custom_paquets.custom_form import AjouterApprenti, ModifierApprenti, ModifierPersonnel
from custom_paquets.custom_form import AjouterPersonnel
from custom_paquets.custom_form import AjouterFormation, ModifierFormation
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


@admin.route("/gestion-personnel", methods=["GET", "POST"])
@admin_login_required
def gestion_personnel():
    """
    Page listant tous les comptes du personnel et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter du personnel
    """
    couleurs = {"SuperAdministrateur": "text-primary", "Educateur Administrateur": "text-warning",
                "Educateur": "text-success", "CIP": "text-info"}
    personnel = get_all_personnel()
    liste_personnel_archive = get_all_personnel(archive=True)
    form_ajouter = AjouterPersonnel()
    form_modifier = ModifierPersonnel()

    if form_modifier.validate_on_submit() and request.method == "POST":
        nouveau_role = request.form.get("nouveau_role")
        nouveau_role = nouveau_role.replace("_", " ")
        identifiant = request.form.get("id-element")
        password = encrypt_password(form_modifier.form_password)
        login = generate_login(form_modifier.form_nom.data, form_modifier.form_prenom.data)
        update_personnel(identifiant, login, form_modifier.form_nom.data, form_modifier.form_prenom.data, form_modifier.form_email.data,
                         password, nouveau_role)
        return redirect(url_for("admin.gestion_personnel"))

    elif form_ajouter.validate_on_submit() and request.method == "POST":
        role = request.form.get("select_role")
        password = encrypt_password(request.form.get('password'))
        login = generate_login(form_ajouter.nom.data, form_ajouter.prenom.data)
        add_personnel(login, form_ajouter.nom.data, form_ajouter.prenom.data, form_ajouter.email.data, password, role)
        return redirect(url_for("admin.gestion_personnel"))

    return render_template("admin/gestion_personnel.html", liste_personnel=personnel, form_ajouter=form_ajouter,
                           form_modifier=form_modifier, couleurs=couleurs, liste_personnel_archive=liste_personnel_archive)


@admin.route("/gestion-apprenti", methods=["GET", "POST"])
@admin_login_required
def gestion_apprenti():
    """
    Page listant tous les comptes des apprentis et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter du personnel
    """

    formations = get_all_formation()
    apprenti = get_all_apprenti()
    liste_apprenti_archivee = get_all_apprenti(archive=True)
    form_ajouter = AjouterApprenti()
    form_modifier = ModifierApprenti()
    if form_modifier.validate_on_submit() and request.method == "POST":
        identifiant = request.form.get("id-element")
        password = encrypt_password(form_modifier.form_password.data)
        login = generate_login(form_modifier.form_nom.data, form_modifier.form_prenom.data)
        
        photo_courante = get_photo_profil_apprenti(identifiant)[14:]
        if photo_courante != request.form.get("avatar"):
            f = request.files.get("avatar")
            chemin_avatar = stocker_photo_profile(f)
        update_apprenti(identifiant, login, form_modifier.form_nom.data, form_modifier.form_prenom.data, password, chemin_avatar)
        return redirect(url_for("admin.gestion_apprenti"))
    
    
    elif form_ajouter.validate_on_submit() and request.method == "POST":
        login = generate_login(form_ajouter.nom.data, form_ajouter.prenom.data)
        f = request.files.get("avatar")
        chemin_avatar = stocker_photo_profile(f)
        id_apprenti = add_apprenti(form_ajouter.nom.data, form_ajouter.prenom.data, login, chemin_avatar)
        add_apprenti_assister(id_apprenti, formations[int(request.form.get("select_formation")) - 1]["id_formation"])
        return redirect(url_for("admin.gestion_apprenti"))

    return render_template("admin/gestion_apprentis.html", liste_apprenti=apprenti, form_ajouter=form_ajouter,
                           form_modifier = form_modifier, formations=formations, liste_apprenti_archivee=liste_apprenti_archivee)


@admin.route("/gestion-formation", methods=["GET", "POST", "DELETE"])
@admin_login_required
def gestion_formation():
    """
    Page listant toutes les formations et permettant de supprimer ou modifier leurs informations
    On peut aussi y rajouter une formation
    """
    formation = get_all_formation()
    liste_formation_archivee = get_all_formation(archive=True)
    form = AjouterFormation()
    form_modifier = ModifierFormation()
    if form.validate_on_submit() and request.method == "POST":
        f = request.files.get("image")
        if f:
            chemin_image = "./static/images/formation_image/" + secure_filename(f.filename)
            f.save(chemin_image)
            chemin_image = "formation_image/" + secure_filename(f.filename)
        else:
            chemin_image = "formation_image/" + "defaut_formation.jpg"
        add_formation(form.intitule.data, form.niveau_qualif.data, form.groupe.data, chemin_image)
        return redirect(url_for("admin.gestion_formation"))

    elif form_modifier.validate_on_submit() and request.method == "POST":
        identifiant = request.form.get("id-element")
        
        photo_courante = get_image_formation(identifiant)[14:]
        if photo_courante != request.form.get("image"):
            f = request.files.get("image")
            chemin_image = stocker_photo_profile(f)
        update_formation(identifiant, form_modifier.form_intitule.data, form_modifier.form_niveau_qualif.data, form_modifier.form_groupe.data, chemin_image)
        return redirect(url_for("admin.gestion_formation"))
    
    return render_template("admin/gestion_formations.html", liste_formation=formation, form=form,
                           form_modifier = form_modifier, liste_formation_archivee=liste_formation_archivee)
