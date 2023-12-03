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
from custom_paquets.file_getter import get_flat
from model.apprenti import get_apprenti_by_login, check_password_apprenti, get_nbr_essaie_connexion_apprenti, \
    check_apprenti
from model.session import get_apprentis_by_formation
from model.formation import get_all_formation
from model.personnel import check_personnel, check_password, get_role, get_nbr_essaie_connexion_personnel

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
    """
    Page de connexion du personnel. Une fois authentifié, la personne, en fonction de son rôle
    aura accès à un panneau de possibilités différentes.

    :return: en fonction du rôle de la personne, on est redirigé vers la page correspondante.
    """
    form = LoginPersonnelForm()
    code = 200
    if form.validate_on_submit():
        if not check_personnel(form.login.data):
            flash("Compte inconnu ou mot de passe invalide.", "error")
            code = 403
        elif not check_password(form.login.data, form.password.data):
            if get_nbr_essaie_connexion_personnel(form.login.data) == 3:
                flash("Compte bloqué, contacter un admin", "error")
                code = 403
            else:
                flash("Compte inconnu ou mot de passe invalide.", "error")
                code = 403
        else:
            if get_nbr_essaie_connexion_personnel(form.login.data) == 3:
                flash("Compte bloqué, contacter un admin", "error")
                code = 403
            else:
                session["name"] = form.login.data
                session["role"] = get_role(form.login.data)
                flash("Connexion réussie.")
                if session["role"] == 'SuperAdministrateur':
                    return redirect(url_for("admin.accueil_admin"))
                else:
                    return redirect(url_for("personnel.choix_formation"))
    return render_template("auth/connexion_personnel.html", form=form), code


@auth.route("/choix-formation-apprentis", methods=["GET", "POST"])
def choix_formation_apprentis():
    """
    Suit la page d'index, permet de charger la liste des toutes les formations dans la page dédiée.

    :return: Rendu de la page choix_formation_apprentis.html avec la liste des formations.
    """
    formations = get_all_formation()
    return render_template("auth/choix_formation_apprentis.html", formations=formations), 200


@auth.route("/choix-eleve-apprentis/<nom_formation>", methods=["GET", "POST"])
def choix_eleve_apprentis(nom_formation):
    """
    Suite la page du choix de la formation pour les apprentis, affiche tous les apprentis associés à cette formation.

    :param nom_formation: Permet de chercher la liste des apprentis en fonction de la formation suivie.
    :return: Rendue de la page choix_apprentis.html avec la liste des eleves associés à la formation.
    """
    apprentis = get_apprentis_by_formation(nom_formation)
    return render_template("auth/choix_apprentis.html", apprentis=apprentis), 200


@auth.route("/connexion-apprentis/<login_apprenti>", methods=["GET", "POST"])
def connexion_apprentis(login_apprenti):
    """
    Page d'authentification des apprentis. Ils doivent résoudre le schéma pour accéder 
    à la page de toutes les fiches techniques qu'ils ont réalisé

    :return: connexion_apprentis.html
    """
    apprenti = get_apprenti_by_login(login_apprenti)
    code = 200
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("pass")
        if check_apprenti(login) and check_password_apprenti(login, password):
            session["name"] = login
            session["role"] = "apprentis"
            flash("Connexion réussie.")
            return redirect(url_for("apprenti.redirection_connexion"))
        else:
            if get_nbr_essaie_connexion_apprenti(login) == 5:
                flash("Compte bloqué, contacter un admin", "error")
                code = 403
            else:
                flash("Compte inconnu ou mot de passe invalide.", "error")
                code = 403
    return render_template("auth/connexion_apprentis.html", apprenti=apprenti), code


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Permet de se déconnecter de la session en cours.

    :return: Redirection vers la page d'index
    """
    session.pop('role', None)
    session.pop('name', None)
    flash("Déconnexion réussie.")
    return redirect(url_for("auth.choix_connexion"))
