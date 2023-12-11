from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from custom_paquets.builder import build_categories
from custom_paquets.custom_form import AjouterFiche
from custom_paquets.decorateur import educadmin_login_required
from model.apprenti import get_apprenti_by_login
from model.ficheintervention import get_fiches_techniques_finies_par_login, assigner_fiche_dummy_eleve

educ_admin = Blueprint("educ_admin", __name__, url_prefix="/educ-admin")

'''
Blueprint pour toutes les routes relatives aux URL des pages des educs admin

Préfixe d'URL : /educ-admin/ .
'''


@educ_admin.route("/<apprenti>/fiches", methods=["GET"])
@educadmin_login_required
def fiches_apprenti(apprenti):
    """
    Récupère toutes les fiches techniques de l'élève sélectionné et les affiche.

    Permet de sélectionner une fiche technique réalisée par un apprenti. 

    :return: rendu de la page choix_fiches_apprenti.html
    """
    apprenti_infos = get_apprenti_by_login(apprenti)
    fiches = get_fiches_techniques_finies_par_login(apprenti)
    return render_template("educ_admin/choix_fiches_apprenti.html", apprenti=apprenti_infos, fiches=fiches)


@educ_admin.route("/<apprenti>/ajouter-fiche", methods=["GET", "POST"])
@educadmin_login_required
def ajouter_fiche(apprenti):
    """
    Page de personnalisation les textes d'une fiche technique.

    :return: rendu de la page personnaliser_fiche_texte_champs.html
    """
    form = AjouterFiche()
    degres = ["rouge", "orange", "jaune", "vert"]
    if form.validate_on_submit():
        degres = request.form.get('degres_urgence')
        assigner_fiche_dummy_eleve(apprenti, session["name"], form.dateinput.data, form.nominput.data,
                                   form.lieuinput.data, form.decriptioninput.data, degres.index(degres) + 1, degres)
        flash("Fiche enregistrée avec succès")
        return redirect(url_for("educ_admin.personnalisation"))
    return render_template('educ_admin/ajouter_fiche.html', form=form, apprenti=apprenti), 200


@educ_admin.route("/personnalisation", methods=["GET"])
@educadmin_login_required
def personnalisation():
    """
    Page de personnalisation les textes d'une fiche technique.

    :return: rendu de la page personnaliser_fiche_texte_champs.html
    """
    liste_police = ["Arial", "Courier New", "Times New Roman", "Verdana", "Impact", "Montserrat", "Roboto", "Open Sans",
                    "Lato", "Oswald", "Poppins"]
    composer_fiche = build_categories(14)
    return render_template('educ_admin/personnaliser_fiche_texte_champs.html', polices=liste_police,
                           composition=composer_fiche), 200
