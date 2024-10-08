from flask import Blueprint, redirect, render_template, session, url_for

from custom_paquets.decorateur import personnel_login_required
from custom_paquets.gestion_filtres_routes import apprenti_existe, formation_existe
from custom_paquets.gestion_image import default_image_formation, default_image_profil
from model.apprenti import Apprenti
from model.formation import Formation
from model.personnel import Personnel

personnel = Blueprint("personnel", __name__, url_prefix="/personnel")

"""
Blueprint pour toutes les routes relatives aux URL des pages du personnel (non super admin)

Préfixe d'URL : /personnel/ .
"""


@personnel.route("/", methods=["GET"])
@personnel.route("/choix-formation-personnel", methods=["GET"])
@personnel_login_required
def choix_formation():
    """
    Page du choix de formation par le personnel.
    Choix de la formation pour ensuite accéder à l'ensemble des apprentis suivant cette formation.

    :return: rendu de la page choix_formation.html
    """
    formations = Formation.get_all_formations()
    # Gestion des images par défaut
    for formation in formations:
        formation.image = default_image_formation(formation.image)
    return render_template("personnel/choix_formation.html", formations=formations), 200


@personnel.route("/choix-eleves/<string:nom_formation>", methods=["GET"])
@personnel_login_required
def choix_eleve(nom_formation):
    """
    Page d'affichage des apprentis d'une formation sélectionnée.
    Permet d'accéder aux fiches techniques des apprentis.

    :return: rendu de la page choix_apprentis.html
    """

    formation_existe(nom_formation)
    id_formation = Formation.get_formation_id_par_nom_formation(nom_formation)
    apprentis = Apprenti.get_apprentis_by_formation(id_formation)
    # Gestion des images par défaut
    for apprenti in apprentis:
        apprenti.photo = default_image_profil(apprenti.photo)
    return render_template("personnel/choix_apprentis.html", apprentis=apprentis), 200


@personnel.route("/redirection-fiches/<string:apprenti>", methods=["GET"])
@personnel_login_required
def redirection_fiches(apprenti):
    """
    Redirection en fonction du rôle du personnel.
    Affiche les actions possibles de la CIP ou les fiches des apprentis si le rôle est éducateur simple
    ou éducateur admin.
    """

    apprenti_existe(apprenti)

    role = Personnel.get_role_by_login(session.get("name"))
    if role == "Educateur Administrateur":
        return redirect(url_for("educ_admin.accueil_educadmin", apprenti=apprenti))
    elif role == "Educateur":
        return redirect(url_for("educ_simple.fiches_apprenti", apprenti=apprenti))
    else:
        return redirect(url_for("cip.affiche_choix", apprenti=apprenti))
