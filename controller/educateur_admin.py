from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from custom_paquets.builder import build_categories, build_pictogrammes
from custom_paquets.converter import changer_date
from custom_paquets.custom_form import AjouterFiche, ModifierCours
from custom_paquets.custom_form import AjouterCours
from custom_paquets.decorateur import educadmin_login_required
from model.apprenti import get_apprenti_by_login, get_id_apprenti_by_login
from model.composer import modifier_composition
from model.ficheintervention import assigner_fiche_dummy_eleve, get_fiches_par_id_fiche, \
    get_proprietaire_fiche_par_id_fiche, copier_fiche, get_fiches_techniques_par_login
from model.formation import get_all_formation, get_formation_id
from model.cours import get_all_cours, get_cours_par_apprenti, get_apprentis_by_formation, update_cours, add_cours
from model.trace import get_commentaires_par_fiche

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
    formations = get_all_formation()
    return render_template("educ_admin/choix_formation.html", formations=formations), 200


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
    formations = get_all_formation()
    form_ajouter = AjouterCours()

    if form_modifier.validate_on_submit() and request.method == "POST":
        identifiant = request.form.get("id-element")
        update_cours(identifiant, form_modifier.form_theme.data, form_modifier.form_cours.data, form_modifier.form_duree.data, form_modifier.select_formation.data)
        return redirect(url_for("educ_admin.gestion_cours"), 302)
    
    elif form_ajouter.validate_on_submit() and request.method == "POST":
        selected_formation_id = request.form.get('select_formation')
        add_cours(form_ajouter.theme.data, form_ajouter.cours.data, form_ajouter.duree.data, selected_formation_id)
        return redirect(url_for("educ_admin.gestion_cours"), 302)
    
    return render_template("educ_admin/gestion_cours.html", cours=cours,
                           form_modifier = form_modifier, form_ajouter=form_ajouter, coursArchives = coursArchives, formations = formations), 200


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
    apprenti_infos = get_apprenti_by_login(apprenti)
    fiches = get_fiches_techniques_par_login(apprenti)
    fiches = changer_date(fiches)
    return render_template("educ_admin/choix_fiches_apprenti.html", apprenti=apprenti_infos, fiches=fiches)


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
        id_fiche = assigner_fiche_dummy_eleve(apprenti, session["name"], form.dateinput.data, form.nominput.data,
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
    liste_polices = ["Arial", "Courier New", "Times New Roman", "Verdana", "Impact", "Montserrat", "Roboto", "Open Sans",
                    "Lato", "Oswald", "Poppins"]
    liste_pictogrammes = build_pictogrammes()
    composer_fiche = build_categories(id_fiche)
    fiche = get_fiches_par_id_fiche(id_fiche)
    if request.method == 'POST':
        modifier_composition(request.form, id_fiche)
        flash("Fiche enregistrée avec succès")
        return redirect(url_for("educ_admin.fiches_apprenti", apprenti=get_proprietaire_fiche_par_id_fiche(id_fiche)), 302)
    return render_template('educ_admin/personnaliser_fiche_texte_champs.html', polices=liste_polices,
                           composition=composer_fiche, liste_pictogrammes=liste_pictogrammes, fiche=fiche), 200


@educ_admin.route("/<apprenti>/<fiche>/commentaires", methods=["GET"])
@educadmin_login_required
def visualiser_commentaires(apprenti, fiche):
    """
    Page d'affichage des commentaires de la fiche d'identifiant fiche de l'apprenti au login apprenti

    :return: les commentaires de la fiche de l'élève sélectionnée.
    """

    commentaires = get_commentaires_par_fiche(fiche)
    return render_template("personnel/commentaires.html", apprenti=apprenti, fiche=fiche,
                           commentaires=commentaires), 200
    