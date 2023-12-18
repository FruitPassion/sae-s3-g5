from flask import Blueprint, render_template, session, redirect, url_for

from model.formation import get_all_formation
from model.session import get_apprentis_by_formation
from custom_paquets.decorateur import personnel_login_required
from model.personnel import get_role

personnel = Blueprint("personnel", __name__, url_prefix="/personnel")

'''
Blueprint pour toutes les routes relatives aux URL des pages du personnel (non super admin)

Préfixe d'URL : /personnel/ .
'''


@personnel.route("/choix-formation-personnel", methods=["GET"])
@personnel_login_required
def choix_formation():
    """
    Page du choix de formation par le personnel.
    Choix de la formation pour ensuite accéder à l'ensemble des apprentis suivant cette formation. 
    
    :return: rendu de la page choix_formation.html
    """
    print(session.get("name"))
    formations = get_all_formation()
    return render_template("personnel/choix_formation.html", formations=formations), 200


@personnel.route("/choix-eleves/<nom_formation>", methods=["GET"])
@personnel_login_required
def choix_eleve(nom_formation):
    """
    Page d'affichage des apprentis d'une formation sélectionnée.
    Permet d'accéder aux fiches techniques des apprentis.

    :return: rendu de la page choix_apprentis.html
    """
    apprentis = get_apprentis_by_formation(nom_formation)
    return render_template("personnel/choix_apprentis.html", apprentis=apprentis), 200


@personnel.route("/redirection-fiches/<apprenti>", methods=["GET"])
@personnel_login_required
def redirection_fiches(apprenti):
    """
    Redirection en fonction du rôle du personnel.
    Affiche les actions possibles de la CIP ou les fiches des apprentis si le rôle est éducateur simple
    ou éducateur admin.
    """

    role = get_role(session.get("name"))
    if role == "Educateur Administrateur":
        return redirect(url_for('educ_admin.fiches_apprenti', apprenti=apprenti))
    elif role == "Educateur":
        return redirect(url_for('educ_simple.fiches_apprenti', apprenti=apprenti))
    else:
        return redirect(url_for('cip.affiche_choix', apprenti=apprenti))
