from flask import Blueprint, Response, redirect, render_template, session, request, url_for

from custom_paquets.builder import build_categories, build_materiel, check_ressenti
from custom_paquets.converter import changer_date
from custom_paquets.custom_form import CompleterFiche
from custom_paquets.decorateur import apprenti_login_required
from custom_paquets.gestion_image import process_photo
from custom_paquets.gestion_filtres_routes import check_accessibilite_fiche, fiche_by_numero_existe
from model.composer import ComposerPresentation
from model.apprenti import Apprenti
from model.cours import Cours
from model.laissertrace import LaisserTrace
from model.ficheintervention import FicheIntervention

apprenti = Blueprint('apprenti', __name__, url_prefix="/apprenti")


'''
Blueprint pour toutes les routes relatives aux URL des pages d'apprentis

Préfixe d'URL : /apprenti/ .
'''

@apprenti.route("/", methods=["GET"])
@apprenti.route("/redirection-connexion", methods=["GET"])
@apprenti_login_required
def redirection_connexion():
    """
    Page de redirection des apprentis une fois qu'ils sont authentifiés.
    Ils accèdent à la liste de leurs fiches techniques.

    :return: Rendu de la page accueil_apprentis.html
    """
    apprenti_infos = Apprenti.get_apprenti_by_login(session["name"])
    fiches = FicheIntervention.get_fiches_techniques_par_login(session['name'])
    fiches = changer_date(fiches)
    cours = Cours.get_liste_cours_assister(apprenti_infos.id_apprenti)
    return render_template("apprentis/accueil_apprentis.html", fiches=fiches, apprenti=apprenti_infos,
                           get_nom_cours_by_id=Cours.get_nom_cours_by_id, cours=cours)


@apprenti.route("/redirection-connexion/suivi", methods=["GET"])
@apprenti_login_required
def suivi_progression():
    """
    Page de suivi de progression des apprentis
    
    :return: rendu de la page suivi_progression_apprenti.html
    """
    fiches_apprenti = FicheIntervention.get_fiches_techniques_par_login(session['name'])
    etat_fiches = {}
    for fiche in fiches_apprenti:
        etat_fiches[fiche.id_fiche] = FicheIntervention.get_etat_fiche_par_id_fiche(fiche.id_fiche)
    return render_template("apprentis/suivi_progression_apprenti.html", etat_fiches=etat_fiches)


@apprenti.route("/completer-fiche/<int:numero>", methods=["GET", "POST"])
@apprenti_login_required
def completer_fiche(numero):
    """
    Page de complétion d'une fiche technique par un apprenti

    :param numero: id de la fiche technique
    :return: rendu de la page completer_fiche.html
    """
    
    check_accessibilite_fiche(FicheIntervention.get_id_fiche_apprenti(session['name'], numero), 0)
    fiche_by_numero_existe(session['name'], numero)

    form = CompleterFiche()
    avancee = "0"
    composer_fiche = build_categories(FicheIntervention.get_id_fiche_apprenti(session['name'], numero))
    materiaux = build_materiel()
    fiche = FicheIntervention.get_fiche_par_id_fiche(FicheIntervention.get_id_fiche_apprenti(session['name'], numero))

    if request.method == 'POST' and form.validate_on_submit():
        avancee = request.form.get("avancee")
        completer_fiche = {}
        ajouter_materiel = {}

        # Gestion des photos
        photo_avant = request.files.get("photo-avant")
        photo_apres = request.files.get("photo-apres")

        if photo_avant.filename != "":
            process_photo(photo_avant, fiche.photo_avant, fiche.id_fiche, 'photo-avant')
            FicheIntervention.definir_photo(fiche.id_fiche, avant_apres=False)  # False pour avant
        if photo_apres.filename != "":
            process_photo(photo_apres, fiche.photo_apres, fiche.id_fiche, 'photo-apres')
            FicheIntervention.definir_photo(fiche.id_fiche, avant_apres=True)  # True pour apres

        # Gestion des checkbox
        checkboxes = ComposerPresentation.get_checkbox_on(fiche.id_fiche)
        for checkbox in checkboxes:
            if checkbox.position_elem not in request.form.keys():
                completer_fiche[f"{checkbox.position_elem}"] = None

        # Gestion des radios
        for element in request.form:
            if "radio-" in element:
                element = request.form.get(f"{element}")
                completer_fiche[f"{element}"] = "radioed"
        radios = ComposerPresentation.get_radio_radioed(fiche.id_fiche)
        for radio in radios:
            if radio.position_elem not in completer_fiche.keys():
                completer_fiche[f"{radio.position_elem}"] = None

        # Gestion des matériaux
        for element in request.form:
            if "selecteur-" in element and len(request.form.get(f"{element}")) != 0:
                ajouter_materiel[f"{element.replace('selecteur-','')}"] = request.form.get(f"{element}")
            elif "selecteur-" in element:
                ajouter_materiel[f"{element.replace('selecteur-','')}"] = None
        if len(ajouter_materiel) != 0:
            ComposerPresentation.maj_materiaux_fiche(ajouter_materiel, fiche.id_fiche)

        # Gestion des autres éléments
        for element in request.form:
            if element == "avancee" or "radio-" in element:
                continue

            if len(request.form.get(f"{element}")) != 0:
                element_data = request.form.get(f"{element}")
            else:
                element_data = None
                
            completer_fiche[f"{element}"] = element_data
        ComposerPresentation.maj_contenu_fiche(completer_fiche, fiche.id_fiche)
        composer_fiche = build_categories(FicheIntervention.get_id_fiche_apprenti(session['name'], numero))

    return Response(render_template("apprentis/completer_fiche.html",  composition=composer_fiche, fiche=fiche,
                           avancee=avancee, materiaux=materiaux, form=form), 200)


@apprenti.route("/imprimer-pdf/<int:numero>", methods=["GET"]) # Pour tester
@apprenti_login_required
def imprimer_pdf(numero):
    """
    Page d'impression d'une fiche technique par un apprenti

    :return: rendu de la page fiche_pdf.html
    """

    fiche_by_numero_existe(session['name'], numero)

    # vérifier que fiche finie
    fiche = FicheIntervention.get_fiche_par_id_fiche(FicheIntervention.get_id_fiche_apprenti(session['name'], numero))
    FicheIntervention.valider_fiche(fiche.id_fiche)

    materiaux = build_materiel()
    composer_fiche = ComposerPresentation.get_composer_presentation_par_apprenti(fiche.id_fiche)
    return render_template("apprentis/fiche_pdf.html", composition=composer_fiche, fiche=fiche,
                           materiaux=materiaux)


@apprenti.route("/valider/<int:numero>", methods=["GET"])
@apprenti_login_required
def valider(numero):
    """
    Page de validation d'une fiche technique par un apprenti

    :return: rendu de la page valider.html
    """
    fiche = FicheIntervention.get_fiche_par_id_fiche(FicheIntervention.get_id_fiche_apprenti(session['name'], numero))
    FicheIntervention.valider_fiche(fiche.id_fiche)
    return redirect(url_for("apprenti.redirection_connexion"))


@apprenti.route("/<int:numero>/commentaires", methods=["GET"])
@apprenti_login_required
def afficher_commentaires(numero):
    """
    Page d'affichage des commentaires par un apprenti de la fiche technique id_fiche

    :return: rendu de la page commentaires.html
    """
    
    check_accessibilite_fiche(FicheIntervention.get_id_fiche_apprenti(session['name'], numero), 1)
    fiche_by_numero_existe(session['name'], numero)

    commentaires = LaisserTrace.get_commentaires_par_fiche(FicheIntervention.get_id_fiche_apprenti(session['name'], numero))
    emoji = build_categories(FicheIntervention.get_id_fiche_apprenti(session['name'], numero))
    ressenti = check_ressenti(emoji)
    return render_template("apprentis/commentaires.html", apprenti=apprenti, numero=numero,
                           commentaires=commentaires, emoji=emoji, ressenti=ressenti), 200


@apprenti.route("/<int:numero>/images", methods=["GET"])
@apprenti_login_required
def afficher_images(numero):
    """
    Page d'affichage des images par un apprenti de la fiche technique id_fiche

    :return: rendu de la page commentaires.html
    """

    fiche_by_numero_existe(session['name'], numero)
        
    fiche = FicheIntervention.get_fiche_par_id_fiche(FicheIntervention.get_id_fiche_apprenti(session['name'], numero))
    return render_template("apprentis/images.html", apprenti=apprenti, numero=numero,
                           fiche=fiche), 200
