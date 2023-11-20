from flask import Blueprint, render_template, session, redirect, url_for
from model.formation import get_all_formation
from model.assister import get_apprentis_by_formation
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
    formations = get_all_formation()
    return render_template("personnel/choix_formation.html", formations=formations)


@personnel.route("/choix-eleves/<nom_formation>", methods=["GET"])
@personnel_login_required
def choix_eleve(nom_formation):
    apprentis = get_apprentis_by_formation(nom_formation)
    return render_template("personnel/choix_apprentis.html", apprentis=apprentis)


@personnel.route("/personnalisation", methods=["GET"])
@personnel_login_required
def personnalisation():
    liste_police = ["Arial", "Courier New", "Times New Roman", "Verdana", "Impact", "Montserrat", "Roboto", "Open Sans",
                    "Lato", "Oswald", "Poppins"]

    return render_template('personnel/personnaliser_fiche_texte_champs.html', polices=liste_police)


@personnel.route("/personnalisation-bis", methods=["GET"])
@personnel_login_required
def personnalisation_bis():
    return render_template('personnel/personnaliser_fiche_couleur_fond.html')


@personnel.route("/redirection-fiches/<apprenti>", methods=["GET"])
@personnel_login_required
def redirection_fiches(apprenti):
    role = get_role(session.get("name"))
    if role == "Educateur Administrateur":
        return redirect(url_for('educ_admin.fiches_apprenti', apprenti=apprenti))
    elif role == "Educateur":
        return redirect(url_for('educ_simple.fiches_apprenti', apprenti=apprenti))
    else:
        return redirect(url_for('cip.affiche_choix', apprenti=apprenti))
