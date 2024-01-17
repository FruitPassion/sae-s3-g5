from flask import Blueprint, redirect, render_template, session, request, url_for

from custom_paquets.builder import build_categories
from custom_paquets.converter import changer_date
from custom_paquets.decorateur import apprenti_login_required
from model.apprenti import get_apprenti_by_login, get_id_apprenti_by_login
from model.composer import get_composer_presentation, get_composer_presentation_par_apprenti, maj_contenu_fiche
from model.apprenti import get_apprenti_by_login
from model.composer import get_composer_presentation, maj_contenu_fiche
from model.trace import ajouter_commentaires_evaluation, get_commentaires_par_fiche
from model.ficheintervention import get_etat_fiche_par_id_fiche, get_fiches_techniques_par_login, get_nom_cours_by_id, \
   get_id_fiche_apprenti, get_fiche_par_id_fiche

apprenti = Blueprint('apprenti', __name__, url_prefix="/apprenti")


'''
Blueprint pour toutes les routes relatives aux URL des pages d'apprentis

Préfixe d'URL : /apprenti/ .
'''


@apprenti.route("/redirection-connexion", methods=["GET"])
@apprenti_login_required
def redirection_connexion():
    """
    Page de redirection des apprentis une fois qu'ils sont authentifiés.
    Ils accèdent à la liste de leurs fiches techniques.

    :return: Rendu de la page accueil_apprentis.html
    """
    apprenti_infos = get_apprenti_by_login(session["name"])
    fiches = get_fiches_techniques_par_login(session['name'])
    fiches = changer_date(fiches)
    return render_template("apprentis/accueil_apprentis.html", fiches=fiches, apprenti=apprenti_infos,
                           get_nom_cours_by_id=get_nom_cours_by_id)


@apprenti.route("/redirection-connexion/suivi", methods=["GET"])
@apprenti_login_required
def suivi_progression():
    """
    Page de suivi de progression des apprentis
    
    :return: rendu de la page suivi_progression_apprenti.html
    """
    fiches_apprenti = get_fiches_techniques_par_login(session['name'])
    etat_fiches = {}
    for fiche in fiches_apprenti:
        etat_fiches[fiche.id_fiche] = get_etat_fiche_par_id_fiche(fiche.id_fiche)
    return render_template("apprentis/suivi_progression_apprenti.html", etat_fiches=etat_fiches)


@apprenti.route("/completer-fiche/<numero>", methods=["GET", "POST"])
@apprenti_login_required
def completer_fiche(numero):
    """
    Page de complétion d'une fiche technique par un apprenti

    :param numero: id de la fiche technique
    :return: rendu de la page completer_fiche.html
    """
    composer_fiche = build_categories(get_id_fiche_apprenti(session['name'], numero))
    fiche = get_fiche_par_id_fiche(get_id_fiche_apprenti(session['name'], numero))
    if request.method == 'POST':
        completer_fiche = {}
        
        completer_fiche["photo_avant"] = request.files.get("photo-avant")
        completer_fiche["photo_apres"] = request.files.get("photo-apres")
            
        for element in request.form:
            if element == "avancee":
                continue
            
            if len(request.form.get(f"{element}")) != 0:
                element_data = request.form.get(f"{element}")
            else:
                element_data = None
                
            if "radio-" in element:
                completer_fiche[f"{element_data}"] = "checked"
            else:
                completer_fiche[f"{element}"] = element_data
                
        maj_contenu_fiche(completer_fiche, fiche.id_fiche)

    return render_template("apprentis/completer_fiche.html",  composition=composer_fiche, fiche=fiche)


@apprenti.route("/imprimer-pdf/<numero>", methods=["GET"]) # Pour tester
@apprenti_login_required
def imprimer_pdf(numero):
    """
    Page d'impression d'une fiche technique par un apprenti

    :return: rendu de la page fiche_pdf.html
    """
    # En attente de la complétion de la fiche
    fiche = get_fiche_par_id_fiche(get_id_fiche_apprenti(session['name'], numero))
    composer_fiche = get_composer_presentation_par_apprenti(get_id_fiche_apprenti(session['name'], numero))
    return render_template("apprentis/fiche_pdf.html", composition=composer_fiche, fiche=fiche)


@apprenti.route("/<id_fiche>/commentaires", methods=["GET"])
@apprenti_login_required
def afficher_commentaires(id_fiche):
    """
    Page d'affichage des commentaires par un apprenti de la fiche technique id_fiche

    :return: rendu de la page commentaires.html
    """
    
    commentaires = get_commentaires_par_fiche(id_fiche)
    return render_template("apprentis/commentaires.html", apprenti=apprenti, id_fiche=id_fiche,
                           commentaires=commentaires), 200
