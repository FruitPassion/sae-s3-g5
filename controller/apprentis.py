from flask import Blueprint, render_template, session

from custom_paquets.builder import build_categories
from custom_paquets.converter import changer_date
from custom_paquets.decorateur import apprenti_login_required
from model.apprenti import get_apprenti_by_login
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
    return render_template("apprentis/accueil_apprentis.html", fiches=fiches, apprenti=apprenti_infos, get_nom_cours_by_id=get_nom_cours_by_id)


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
        etat_fiches[fiche["id_fiche"]] = get_etat_fiche_par_id_fiche(fiche["id_fiche"])
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
    return render_template("apprentis/completer_fiche.html",  composition=composer_fiche, fiche=fiche)

@apprenti.route("/imprimer-pdf", methods=["GET", "POST"])
@apprenti_login_required
def imprimer_pdf():
    """
    Page d'impression d'une fiche technique par un apprenti

    :return: rendu de la page fiche_pdf.html
    """
    return render_template("apprentis/fiche_pdf.html")