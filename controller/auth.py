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
from custom_paquets.decorateur import logout_required
from model.apprenti import get_apprenti_by_login, check_password_apprenti, get_nbr_essaie_connexion_apprenti, \
    check_apprenti, check_password_is_set
from model.cours import get_apprentis_by_formation
from model.formation import get_all_formation
from model.personnel import check_personnel, check_password, get_role, get_nbr_essaie_connexion_personnel, \
    get_liste_personnel_non_super

auth = Blueprint("auth", __name__)

'''
Blueprint pour toutes les routes relatives au authentifications.

Pas de préfice d'URL.
'''

COMPTE_BLOQUE = "Compte bloqué, contacter un admin"
COMPTE_INCONNU = "Compte inconnu ou mot de passe invalide."
CONNEXION_REUSSIE = "Connexion réussie."


@auth.route("/")
@logout_required
def choix_connexion():
    """
    Page par défaut du site. Permet de se diriger vers les pages de connexion en tant qu'apprenti ou en tant que
    personnel.

    :return: rendu de la page index.html
    """
    return render_template("auth/index.html")


@auth.route("/choix-type-connexion")
@logout_required
def choix_type_connexion():
    """
    Page permettant de choisir le type de connexion que l'on souhaite effectuer.

    :return: Rendu de la page choix_type_connexion.html
    """
    return render_template("auth/choix_type_connexion.html")


@auth.route("/connexion-personnel-pin", methods=["GET", "POST"])
@logout_required
def connexion_personnel_pin():
    """
    Page de connexion du personnel. Une fois authentifié, la personne, en fonction de son rôle
    aura accès à un panneau de possibilités différentes.

    :return: En fonction du rôle de la personne, on est redirigé vers la page correspondante.
    """
    personnels = get_liste_personnel_non_super()
    code = 200
    if request.method == "POST":
        passwd = request.form["code"]
        login = request.form.get('login_select')
        if not check_password(login, passwd):
            if get_nbr_essaie_connexion_personnel(login) == 3:
                flash(COMPTE_BLOQUE, "error")
                code = 403
            else:
                flash(COMPTE_INCONNU, "error")
                code = 403
        else:
            if get_nbr_essaie_connexion_personnel(login) == 3:
                flash(COMPTE_BLOQUE, "error")
                code = 403
            else:
                session["name"] = login
                session["role"] = get_role(login)
                flash(CONNEXION_REUSSIE)
                if session["role"] == 'SuperAdministrateur':
                    return redirect(url_for("admin.accueil_admin"), 302)
                elif session["role"] == "Educateur Administrateur":
                    return redirect(url_for('educ_admin.accueil_educadmin'), 302)
                else:
                    return redirect(url_for("personnel.choix_formation"))
    return render_template("auth/connexion_personnel_pin.html", personnels=personnels), code


@auth.route("/connexion-personnel-mdp", methods=["GET", "POST"])
@logout_required
def connexion_personnel_mdp():
    """
    Page de connexion du personnel. Une fois authentifié, la personne, en fonction de son rôle
    aura accès à un panneau de possibilités différentes.

    :return: En fonction du rôle de la personne, on est redirigé vers la page correspondante.
    """
    form = LoginPersonnelForm()
    code = 200
    if form.validate_on_submit():
        if not check_personnel(form.login.data) or form.login.data == "dummy":
            flash(COMPTE_INCONNU, "error")
            code = 403
        elif not check_password(form.login.data, form.password.data):
            if get_nbr_essaie_connexion_personnel(form.login.data) == 3:
                flash(COMPTE_BLOQUE, "error")
                code = 403
            else:
                flash(COMPTE_INCONNU, "error")
                code = 403
        else:
            if get_nbr_essaie_connexion_personnel(form.login.data) == 3:
                flash(COMPTE_BLOQUE, "error")
                code = 403
            else:
                session["name"] = form.login.data
                session["role"] = get_role(form.login.data)
                flash(CONNEXION_REUSSIE)
                if session["role"] == 'SuperAdministrateur':
                    return redirect(url_for("admin.accueil_admin"), 302)
                elif session["role"] == "Educateur Administrateur":
                    return redirect(url_for('educ_admin.accueil_educadmin'), 302)
                else:
                    return redirect(url_for("personnel.choix_formation"), 302)
    return render_template("auth/connexion_personnel_code.html", form=form), code


@auth.route("/choix-formation-apprentis", methods=["GET", "POST"])
@logout_required
def choix_formation_apprentis():
    """
    Suit la page d'index, permet de charger la liste des toutes les formations dans la page dédiée.

    :return: Rendu de la page choix_formation_apprentis.html avec la liste des formations.
    """
    formations = get_all_formation()
    return render_template("auth/choix_formation_apprentis.html", formations=formations), 200


@auth.route("/choix-eleve-apprentis/<nom_formation>", methods=["GET", "POST"])
@logout_required
def choix_eleve_apprentis(nom_formation):
    """
    Suite la page du choix de la formation pour les apprentis, affiche tous les apprentis associés à cette formation.

    :param nom_formation: Permet de chercher la liste des apprentis en fonction de la formation suivie.
    :return: Rendue de la page choix_apprentis.html avec la liste des eleves associés à la formation.
    """
    apprentis = get_apprentis_by_formation(nom_formation)
    return render_template("auth/choix_apprentis.html", apprentis=apprentis, nom_formation=nom_formation), 200


@auth.route("/connexion-apprentis/<nom_formation>/<login_apprenti>", methods=["GET", "POST"])
@logout_required
def connexion_apprentis(nom_formation, login_apprenti):
    """
    Page d'authentification des apprentis. Ils doivent résoudre le schéma pour accéder 
    à la page de toutes les fiches techniques qu'ils ont réalisé

    :return: connexion_apprentis.html
    """
    apprenti = get_apprenti_by_login(login_apprenti)
    code = 200
    code_set = check_password_is_set(login_apprenti)
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("pass")
        if check_apprenti(login) and check_password_apprenti(login, password):
            session["name"] = login
            session["role"] = "apprentis"
            flash(CONNEXION_REUSSIE)
            return redirect(url_for("apprenti.redirection_connexion"), 302)
        else:
            if get_nbr_essaie_connexion_apprenti(login) == 5:
                flash(COMPTE_BLOQUE, "error")
                code = 403
            else:
                flash(COMPTE_INCONNU, "error")
                code = 403
    return render_template("auth/connexion_apprentis.html", apprenti=apprenti,
                           nom_formation=nom_formation, code_set=code_set), code


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Permet de se déconnecter de la session en cours.

    :return: Redirection vers la page d'index
    """
    session.pop('role', None)
    session.pop('name', None)
    flash("Déconnexion réussie.")
    return redirect(url_for("auth.choix_connexion"), 302)
