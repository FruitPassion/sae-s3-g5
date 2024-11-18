import json

from flask import Blueprint, Response, redirect, render_template, request, url_for

from custom_paquets.converter import changer_date
from custom_paquets.decorateur import cip_login_required
from custom_paquets.gestion_filtres_routes import apprenti_existe, fiche_by_id_existe
from model.apprenti import Apprenti
from model.cours import Cours
from model.ficheintervention import FicheIntervention
from model.formation import Formation
from model.laissertrace import LaisserTrace

cip = Blueprint("cip", __name__, url_prefix="/cip")
personnel = Blueprint("personnel", __name__, url_prefix="/cip")

"""
Blueprint pour toutes les routes relatives aux URL des pages du CIP

Préfixe d'URL : /cip/ .
"""


@cip.route("/", methods=["GET"])
@cip.route("/<string:apprenti>/choix-operations", methods=["GET"])
@cip_login_required
def affiche_choix(apprenti):
    """
    Page par défaut de la CIP. Une fois authentifiée, la CIP choisit l'action qu'elle souhaite effectuer
    (visualiser les fiches techniques, suivi de progression ou adaptation situation d'examen)

    :return: rendu de la page choix_operations.html
    """

    apprenti_existe(apprenti)

    formation = Formation.get_formation_par_apprenti(apprenti)
    return render_template("cip/choix_operations.html", apprenti=apprenti, formation=formation), 200


@cip.route("/<string:apprenti>/fiches", methods=["GET"])
@cip_login_required
def fiches_apprenti(apprenti):
    """
    Récupère toutes les fiches techniques de l'apprenti sélectionné et les affiche.

    Permet de consulter les commentaires laissés par les éducateurs et par l'apprenti en question.

    :return: rendu de la page fiches_techniques.html
    """

    apprenti_existe(apprenti)

    apprenti_infos = Apprenti.get_apprenti_by_login(apprenti)
    fiches = FicheIntervention.get_fiches_techniques_finies_par_login(apprenti)
    fiches = changer_date(fiches)
    cours = Cours.get_liste_cours_assister(apprenti_infos.id_apprenti)
    return render_template("cip/fiches_techniques.html", apprenti=apprenti_infos, fiches=fiches, get_nom_cours_by_id=Cours.get_nom_cours_by_id, cours=cours)


@cip.route("/<string:apprenti>/<int:fiche>/commentaires", methods=["GET"])
@cip_login_required
def visualiser_commentaires(apprenti, fiche):
    """
    Page de visualisation des commentaires de la CIP.
    En fonction de l'identifiant de l'élève et de la fiche sélectionnés, affiche les commentaires
    des éducateurs et de l'apprenti.

    :return: rendu de la page commentaires.html
    """

    apprenti_existe(apprenti)
    fiche_by_id_existe(fiche)

    commentaires = LaisserTrace.get_commentaires_par_fiche(fiche)
    return render_template("cip/commentaires.html", commentaires=commentaires, apprenti=apprenti), 200


@cip.route("/<string:apprenti>/suivi-progression", methods=["GET"])
@cip_login_required
def suivi_progression_apprenti(apprenti):
    """
    Page de suivi de progression de l'apprenti sélectionné.
    Affiche le suivi de progression sous forme de graphique (niveau moyen, nombre de fiches finies, niveau des fiches)

    :return: rendu de la page suivi-progression.html
    """

    apprenti_existe(apprenti)

    apprenti_infos = Apprenti.get_apprenti_by_login(apprenti)

    # Récupération des niveaux et états des fiches
    niv_fiche = FicheIntervention.get_niveau_etat_fiches_par_login(apprenti)
    for niv in niv_fiche:
        niv["total_niveau"] = str(niv["total_niveau"])

    niveau_moyen = FicheIntervention.get_niveau_moyen_champs_par_login(apprenti)
    nb_fiches_finies = FicheIntervention.get_nombre_fiches_finies_par_login(apprenti)

    return render_template("cip/suivi_progression_cip.html", niv_fiche=json.dumps(niv_fiche), niveau_moyen=niveau_moyen, nb_fiches_finies=nb_fiches_finies, apprenti=apprenti_infos), 200


@cip.route("/<string:apprenti>/adaptation-situation-examen", methods=["GET"])
@cip_login_required
def affichage_adaptation_situation_examen(apprenti):
    """
    Page de suivi d'adaptation en situation d'examen de l'apprenti sélectionné.
    Affiche le commentaire de la CIP.

    :return: rendu de la page adaptation_situation_examen.html
    """

    apprenti_existe(apprenti)

    commentaire = Apprenti.get_adaptation_situation_examen_par_apprenti(apprenti)
    apprenti = Apprenti.get_apprenti_by_login(apprenti)
    return render_template("cip/adaptation_situation_examen.html", apprenti=apprenti, commentaire=commentaire), 200


@cip.route("/<string:apprenti>/modifier-commentaire", methods=["GET", "POST"])
@cip_login_required
def modifier_commentaire(apprenti):
    """
    Page de modification du commentaire sur un apprenti par la CIP

    :return: la page de modification du commentaire
    """

    apprenti_existe(apprenti)

    commentaire = Apprenti.get_adaptation_situation_examen_par_apprenti(apprenti)

    if request.method == "POST":
        adaptation_situation_examen = request.form["commentaire"]
        Apprenti.update_adaptation_situation_examen_par_apprenti(apprenti, adaptation_situation_examen)

        return redirect(url_for("cip.affichage_adaptation_situation_examen", apprenti=apprenti))
    apprenti = Apprenti.get_apprenti_by_login(apprenti)
    return Response(render_template("cip/modifier_adaptation_situation_examen.html", apprenti=apprenti, commentaire=commentaire), 200)


@cip.route("/<string:apprenti>/ajouter-commentaire", methods=["GET", "POST"])
@cip_login_required
def ajouter_commentaire(apprenti):
    """
    Page d'ajout du commentaire sur un apprenti par la CIP

    :return: la page d'ajout d'un commentaire
    """

    apprenti_existe(apprenti)

    if request.method == "POST":
        adaptation_situation_examen = request.form["commentaire"]
        Apprenti.update_adaptation_situation_examen_par_apprenti(apprenti, adaptation_situation_examen)
        return redirect(url_for("cip.affichage_adaptation_situation_examen", apprenti=apprenti))
    apprenti = Apprenti.get_apprenti_by_login(apprenti)
    return Response(render_template("cip/ajouter_adaptation_situation_examen.html", apprenti=apprenti), 200)
