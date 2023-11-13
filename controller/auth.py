from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
    session,
)

from custom_paquets.custom_form import LoginPersonnelForm
from model.apprenti import getApprentiByLogin, checkPasswordApprenti
from model.assister import getApprentisByFormation
from model.formation import getAllFormation
from model.personnel import checkPersonnel, checkPassword, getRole

auth = Blueprint("auth", __name__)

'''
Blueprint pour toutes les routes relatives au authentifications.

Pas de préfice d'URL.
'''


@auth.route("/")
def choix_connexion():
    """
    Page par défaut du site. Permet de se diriger vers les pages de connexion en tant qu'apprenti ou en tant que
    personnel.

    :return: rendu de la page index.html
    """
    return render_template("auth/index.html")


@auth.route("/connexion-personnel", methods=["GET", "POST"])
def connexion_personnel():
    form = LoginPersonnelForm()
    if form.validate_on_submit():
        if not checkPersonnel(form.login.data) or not checkPassword(
            form.login.data, form.password.data
        ):
            flash("Compte inconnu ou mot de passe erroné.", "error")
        else:
            session["name"] = form.login.data
            session["role"] =  getRole(form.login.data)
            if session["role"] == 'SuperAdministrateur':
                return redirect(url_for("admin.redirection_connexion"))
            else:
                return redirect(url_for("personnel.redirection_connexion"))
    return render_template("auth/connexion_personnel.html", form=form)


@auth.route("/choix-formation-apprentis", methods=["GET", "POST"])
def choix_formation_apprentis():
    """
    Suit la page d'index, permet de charger la liste des toute les formations dans la page dédiée.

    :return: rendu de la page choix_formation_apprentis.html avec la liste des formations.
    """
    formations = getAllFormation()
    return render_template(
        "auth/choix_formation_apprentis.html", formations=formations
    )


@auth.route("/choix-eleve-apprentis/<nom_formation>", methods=["GET", "POST"])
def choix_eleve_apprentis(nom_formation):
    """
    Suite la page du choix de la formation pour les apprentis, affiche tout les apprentis associés à cette formation.

    :param nom_formation: Permet de chercher la liste des apprentis en fonction de la formation suivie.
    :return: rendu de la page choix_apprentis.html avec la liste des eleves associés à la formation.
    """
    apprentis = getApprentisByFormation(nom_formation)
    return render_template("auth/choix_apprentis.html", apprentis=apprentis)


@auth.route("/connexion-apprentis/<login_apprenti>", methods=["GET", "POST"])
def connexion_apprentis(login_apprenti):
    apprenti = getApprentiByLogin(login_apprenti)
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("pass")
        if checkPasswordApprenti(login, password):
            session["name"] = login
            session["role"] = "apprentis"
            return redirect(url_for("apprenti.redirection_connexion"))
        else:
            flash("Compte inconnu ou mot de passe erroné.", "error")
    return render_template("auth/connexion_apprentis.html", apprenti=apprenti)


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Permet de se déconnecter de la session en cour.

    :return: redirection vers la page d'index
    """
    session.pop('role', None)
    return redirect(url_for("auth.choix_connexion"))
