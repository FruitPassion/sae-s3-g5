from flask import Blueprint, redirect, render_template, request, url_for

from custom_paquets.converter import changer_date
from custom_paquets.decorateur import cip_login_required
from model.formation import get_formation_par_apprenti
from model.trace import get_commentaires_par_fiche
from model.apprenti import get_apprenti_by_login, get_adaptation_situation_examen_par_apprenti, \
    update_adaptation_situation_examen_par_apprenti
from model.ficheintervention import get_fiches_techniques_finies_par_login, get_niveau_etat_fiches_par_login, \
    get_niveau_moyen_champs_par_login, get_nombre_fiches_finies_par_login, get_nom_cours_by_id
import json

cip = Blueprint("cip", __name__, url_prefix="/cip")

'''
Blueprint pour toutes les routes relatives aux URL des pages du CIP

Préfixe d'URL : /cip/ .
'''


@cip.route("/<apprenti>/choix-operations", methods=["GET"])
@cip_login_required
def affiche_choix(apprenti):
    """
    Page par défaut de la CIP. Une fois authentifiée, la CIP choisit l'action qu'elle souhaite effectuer
    (visualiser les fiches techniques, suivi de progression ou adaptation situation d'examen)

    :return: rendu de la page choix_operations.html
    """
    formation = get_formation_par_apprenti(apprenti)
    return render_template("cip/choix_operations.html", apprenti=apprenti,
                           formation=formation), 200


@cip.route("/<apprenti>/fiches", methods=["GET"])
@cip_login_required
def fiches_apprenti(apprenti):
    """
    Récupère toutes les fiches techniques de l'apprenti sélectionné et les affiche.

    Permet de consulter les commentaires laissés par les éducateurs et par l'apprenti en question. 

    :return: rendu de la page fiches_techniques.html
    """
    apprenti_infos = get_apprenti_by_login(apprenti)
    fiches = get_fiches_techniques_finies_par_login(apprenti)
    fiches = changer_date(fiches)
    return render_template("cip/fiches_techniques.html", apprenti=apprenti_infos, fiches=fiches,
                           get_nom_cours_by_id=get_nom_cours_by_id)


@cip.route("/<apprenti>/<fiche>/commentaires", methods=["GET"])
@cip_login_required
def visualiser_commentaires(apprenti, fiche):
    """
    Page de visualisation des commentaires de la CIP.
    En fonction de l'identifiant de l'élève et de la fiche sélectionnés, affiche les commentaires 
    des éducateurs et de l'apprenti. 
    
    :return: rendu de la page commentaires.html
    """
    commentaires = get_commentaires_par_fiche(fiche)
    return render_template("cip/commentaires.html", commentaires=commentaires, apprenti=apprenti), 200


@cip.route("/<apprenti>/suivi-progression", methods=["GET"])
@cip_login_required
def suivi_progression_apprenti(apprenti):
    """
    Page de suivi de progression de l'apprenti sélectionné. 
    Affiche le suivi de progression sous forme de graphique (niveau moyen, nombre de fiches finies, niveau des fiches)

    :return: rendu de la page suivi-progression.html
    """
    apprenti_infos = get_apprenti_by_login(apprenti)

    # Récupération des niveaux et états des fiches
    niv_fiche = get_niveau_etat_fiches_par_login(apprenti)
    for niv in niv_fiche:
        niv["total_niveau"] = str(niv["total_niveau"])

    niveau_moyen = get_niveau_moyen_champs_par_login(apprenti)
    nb_fiches_finies = get_nombre_fiches_finies_par_login(apprenti)

    return render_template("cip/suivi_progression_cip.html", niv_fiche=json.dumps(niv_fiche),
                           niveau_moyen=niveau_moyen, nb_fiches_finies=nb_fiches_finies, apprenti=apprenti_infos), 200


@cip.route("/<apprenti>/adaptation-situation-examen", methods=["GET"])
@cip_login_required
def affichage_adaptation_situation_examen(apprenti):
    """
    Page de suivi d'adaptation en situation d'examen de l'apprenti sélectionné. 
    Affiche le commentaire de la CIP.
    
    :return: rendu de la page adaptation_situation_examen.html
    """

    commentaire = get_adaptation_situation_examen_par_apprenti(apprenti)
    apprenti = get_apprenti_by_login(apprenti)
    return render_template("cip/adaptation_situation_examen.html", apprenti=apprenti,
                           commentaire=commentaire), 200


@cip.route("/<apprenti>/modifier-commentaire", methods=["GET", "POST"])
@cip_login_required
def modifier_commentaire(apprenti):
    """
    Page de modification du commentaire sur un apprenti par la CIP
    
    :return: la page de modification du commentaire 
    """

    commentaire = get_adaptation_situation_examen_par_apprenti(apprenti)

    if request.method == 'POST':
        adaptation_situation_examen = request.form["commentaire"]
        update_adaptation_situation_examen_par_apprenti(apprenti, adaptation_situation_examen)

        return redirect(url_for('cip.affichage_adaptation_situation_examen', apprenti=apprenti), 200)
    apprenti = get_apprenti_by_login(apprenti)
    return render_template("cip/modifier_adaptation_situation_examen.html", apprenti=apprenti,
                           commentaire=commentaire), 200


@cip.route("/<apprenti>/ajouter-commentaire", methods=["GET", "POST"])
@cip_login_required
def ajouter_commentaire(apprenti):
    """
    Page d'ajout du commentaire sur un apprenti par la CIP
    
    :return: la page d'ajout d'un commentaire 
    """
    if request.method == 'POST':
        adaptation_situation_examen = request.form["commentaire"]
        update_adaptation_situation_examen_par_apprenti(apprenti, adaptation_situation_examen)
        return redirect(url_for('cip.affichage_adaptation_situation_examen', apprenti=apprenti), 200)
    apprenti = get_apprenti_by_login(apprenti)
    return render_template("cip/ajouter_adaptation_situation_examen.html", apprenti=apprenti), 200
