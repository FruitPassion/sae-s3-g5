from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from custom_paquets.builder import build_categories, build_pictogrammes
from custom_paquets.converter import changer_date
from custom_paquets.custom_form import AjouterFiche, AjouterPicto, ModifierCours, ModifierMateriel, ModifierPicto
from custom_paquets.custom_form import AjouterCours, AjouterMateriel
from custom_paquets.decorateur import educadmin_login_required
from custom_paquets.gestion_image import stocker_photo_materiel, stocker_photo_profile, stocker_picto
from model.apprenti import get_apprenti_by_login, get_id_apprenti_by_login
from model.composer import modifier_composition
from model.ficheintervention import assigner_fiche_dummy_eleve, \
    get_proprietaire_fiche_par_id_fiche, copier_fiche, get_fiches_techniques_par_login, get_nom_cours_by_id, \
    get_fiche_par_id_fiche, get_id_fiche_apprenti
from model.formation import get_all_formations, get_formation_par_apprenti
from model.cours import get_all_cours, get_cours_par_apprenti, get_apprentis_by_formation, update_cours, add_cours
from model.materiel import add_materiel, get_all_categories_materiel, get_all_materiel, get_photo_materiel, update_materiel
from model.personnel import get_id_personnel_by_login
from model.pictogramme import add_picto, get_all_categories_pictos, get_all_pictogrammes, get_photo_picto_by_id, update_picto
from model.trace import get_commentaires_par_fiche, get_commentaires_type_par_fiche

educ_admin = Blueprint("educ_admin", __name__, url_prefix="/educ-admin")

'''
Blueprint pour toutes les routes relatives aux URL des pages des educs admin

Préfixe d'URL : /educ-admin/ .
'''


@educ_admin.route("/accueil-educadmin", methods=["GET"])
@educadmin_login_required
def accueil_educadmin():
    """
    Page vers laquelle est redirigé l'educ admin
    """
    return render_template("educ_admin/accueil_educadmin.html")


@educ_admin.route("/choix-formation", methods=["GET"])
@educadmin_login_required
def choix_formation():
    """
    Page du choix de formation par le personnel.
    Choix de la formation pour ensuite accéder à l'ensemble des apprentis suivant cette formation.

    :return: rendu de la page choix_formation.html
    """
    formations = get_all_formations()
    return render_template("educ_admin/choix_formation.html", formations=formations), 200


@educ_admin.route("/gestion-images", methods=["GET", "POST"])
@educadmin_login_required
def gestion_images():
    """
    Page du choix de gestion des images des matériaux
    """
    materiaux = get_all_materiel()
    form_ajouter = AjouterMateriel()
    form_modifier = ModifierMateriel()

    categories_materiaux = get_all_categories_materiel()
    
    categories = []
    for categorie in categories_materiaux:
        categories.append(categorie[0])


    if form_modifier.validate_on_submit() and request.method == "POST":
        identifiant = request.form.get("id-element")[5:]
        categorie = request.form.get("categorie-modifier")
        if len(request.files.get("materiel-modifier").filename) != 0:
            f = request.files.get("materiel-modifier")
            chemin_materiel = stocker_photo_materiel(f, categorie=categorie)
        else:
            chemin_materiel = get_photo_materiel(identifiant)
        update_materiel(identifiant, form_modifier.form_modifier_nom.data, categorie, chemin_materiel)
        return redirect(url_for("educ_admin.gestion_images"), 302)

    elif form_ajouter.validate_on_submit() and request.method == "POST":
        f = request.files.get("materiel")
        categorie = request.form.get("categorie-ajouter")
        chemin_materiel = stocker_photo_materiel(f, categorie=categorie)
        add_materiel(form_ajouter.nom.data, categorie, chemin_materiel)
        return redirect(url_for("educ_admin.gestion_images"), 302)

    return render_template("educ_admin/gestion_materiaux.html", materiaux=materiaux,
                           form_ajouter=form_ajouter, categories = categories,
                           form_modifier=form_modifier), 200


@educ_admin.route("/gestion-pictos", methods=["GET", "POST"])
@educadmin_login_required
def gestion_pictos():
    """
    Page du choix de gestion des images des matériaux
    """
    pictos = get_all_pictogrammes()
    categories_pictos = get_all_categories_pictos()
    categories = []
    for categorie in categories_pictos:
        categories.append(categorie[0])

    form_ajouter = AjouterPicto()
    form_modifier = ModifierPicto()

    if form_ajouter.validate_on_submit() and request.method == "POST":
        f = request.files.get("picto")
        chemin_picto = stocker_picto(f)
        categorie = request.form.get("categorie-ajouter")
        print(categorie)
        add_picto(form_ajouter.label.data, categorie, form_ajouter.souscategorie.data, chemin_picto)
        return redirect(url_for("educ_admin.gestion_pictos"), 302)

    elif form_modifier.validate_on_submit() and request.method == "POST":
        identifiant = request.form.get("id-element")[5:]

        if len(request.files.get("picto-modifier").filename) != 0:
            f = request.files.get("picto-modifier")
            chemin_picto = stocker_picto(f)
        else:
            chemin_picto = get_photo_picto_by_id(identifiant)
        update_picto(identifiant, form_modifier.form_modifier_label.data, form_modifier.form_modifier_categorie.data,
                     form_modifier.form_modifier_souscategorie.data, chemin_picto)
        return redirect(url_for("educ_admin.gestion_pictos"), 302)

    return render_template("educ_admin/gestion_pictos.html", pictos=pictos, form_modifier=form_modifier,
                           form_ajouter=form_ajouter, categories = categories), 200


@educ_admin.route("/gestion-cours", methods=["GET", "POST", "DELETE"])
@educadmin_login_required
def gestion_cours():
    """
    Page listant tous les cours et permettant de les supprimer, modifier, archiver et désarchiver.
    On peux également rajouter des cours.
    
    :return: rendu de la page gestion_cours.html
    """
    cours = get_all_cours()
    coursArchives = get_all_cours(archive=True)
    form_modifier = ModifierCours()
    formations = get_all_formations()
    form_ajouter = AjouterCours()

    if form_modifier.validate_on_submit() and request.method == "POST":
        identifiant = request.form.get("id-element")
        update_cours(identifiant, form_modifier.form_theme.data, form_modifier.form_cours.data,
                     form_modifier.form_duree.data, form_modifier.select_formation.data)
        return redirect(url_for("educ_admin.gestion_cours"), 302)

    elif form_ajouter.validate_on_submit() and request.method == "POST":
        selected_formation_id = request.form.get('select_formation')
        add_cours(form_ajouter.theme.data, form_ajouter.cours.data, form_ajouter.duree.data, selected_formation_id)
        return redirect(url_for("educ_admin.gestion_cours"), 302)

    return render_template("educ_admin/gestion_cours.html", cours=cours,
                           form_modifier=form_modifier, form_ajouter=form_ajouter, coursArchives=coursArchives,
                           formations=formations), 200


@educ_admin.route("/choix-eleve/<nom_formation>", methods=["GET"])
@educadmin_login_required
def choix_eleve(nom_formation):
    """
    Page d'affichage des apprentis d'une formation sélectionnée.
    Permet d'accéder aux fiches techniques des apprentis de cette formation.

    :return: rendu de la page choix_apprentis.html
    """
    apprentis = get_apprentis_by_formation(nom_formation)
    return render_template("educ_admin/choix_apprentis.html", apprentis=apprentis), 200


@educ_admin.route("/<apprenti>/fiches", methods=["GET"])
@educadmin_login_required
def fiches_apprenti(apprenti):
    """
    Récupère toutes les fiches techniques de l'apprenti sélectionné et les affiche.

    Permet de sélectionner une fiche technique réalisée par un apprenti. 

    :return: rendu de la page choix_fiches_apprenti.html
    """
    formation = get_formation_par_apprenti(apprenti)
    apprenti_infos = get_apprenti_by_login(apprenti)
    fiches = get_fiches_techniques_par_login(apprenti)
    fiches = changer_date(fiches)
    return render_template("educ_admin/choix_fiches_apprenti.html", apprenti=apprenti_infos,
                           fiches=fiches, get_nom_cours_by_id=get_nom_cours_by_id, formation=formation)


@educ_admin.route("/modifier-fiche/<id_fiche>", methods=["GET"])
@educadmin_login_required
def modifier_fiche(id_fiche):
    """
    Modifie la fiche d'identifiant id_fiche.
    Effectue une copie de cette fiche (rendue inutilisable) et redirige vers la page de
    personnalisation de la fiche.

    :return: rendu de la page personnaliser_fiche_texte_champs.html
    """
    id_fiche = copier_fiche(id_fiche, session["name"])
    flash("Fiche copiée avec succès")
    return redirect(url_for("educ_admin.personnalisation", id_fiche=id_fiche))


@educ_admin.route("/<apprenti>/ajouter-fiche", methods=["GET", "POST"])
@educadmin_login_required
def ajouter_fiche(apprenti):
    """
    Page d'ajout d'une fiche technique pour un apprenti.

    Permet la personnalisation des items.

    :return: rendu de la page ajouter_fiche.html
    """
    form = AjouterFiche()
    cours = get_cours_par_apprenti(get_id_apprenti_by_login(apprenti))
    if form.validate_on_submit():
        degres = request.form.get('degres_urgence')
        id_cours = request.form.get('coursinput')
        id_personnel = get_id_personnel_by_login(session["name"])
        id_fiche = assigner_fiche_dummy_eleve(apprenti, id_personnel, form.dateinput.data, form.nominput.data,
                                              form.lieuinput.data, form.decriptioninput.data, degres.index(degres) + 1,
                                              degres, form.nomintervenant.data, form.prenomintervenant.data, id_cours)
        flash("Fiche enregistrée avec succès")
        return redirect(url_for("educ_admin.personnalisation", id_fiche=id_fiche), 302)
    return render_template('educ_admin/ajouter_fiche.html', form=form, apprenti=apprenti,
                           cours=cours), 200


@educ_admin.route("/personnalisation/<id_fiche>", methods=["GET", "POST"])
@educadmin_login_required
def personnalisation(id_fiche):
    """
    Page de personnalisation des textes d'une fiche technique.

    :return: rendu de la page personnaliser_fiche_texte_champs.html
    """
    liste_polices = ["Arial", "Courier New", "Times New Roman", "Verdana", "Impact", "Montserrat", "Roboto",
                     "Open Sans",
                     "Lato", "Oswald", "Poppins"]
    liste_pictogrammes = build_pictogrammes()
    composer_fiche = build_categories(id_fiche)
    fiche = get_fiche_par_id_fiche(id_fiche)
    if request.method == 'POST':
        modifier_composition(request.form, id_fiche)
        flash("Fiche enregistrée avec succès")
        return redirect(url_for("educ_admin.fiches_apprenti", apprenti=get_proprietaire_fiche_par_id_fiche(id_fiche)),
                        302)
    return render_template('educ_admin/personnaliser_fiche_texte_champs.html', polices=liste_polices,
                           composition=composer_fiche, liste_pictogrammes=liste_pictogrammes, fiche=fiche), 200


@educ_admin.route("/<apprenti>/<numero>/commentaires", methods=["GET"])
@educadmin_login_required
def visualiser_commentaires(apprenti, numero):
    """
    Page d'affichage des commentaires de la fiche d'identifiant fiche de l'apprenti au login apprenti

    :return: les commentaires de la fiche de l'élève sélectionnée.
    """
    commentaires_educ = get_commentaires_type_par_fiche((get_id_fiche_apprenti(apprenti, numero)))
    commentaires_appr = get_commentaires_type_par_fiche((get_id_fiche_apprenti(apprenti, numero)), apprenti="1")
    return render_template("personnel/commentaires.html", apprenti=apprenti, numero=numero,
                           commentaires_educ=commentaires_educ, commentaires_appr=commentaires_appr), 200
