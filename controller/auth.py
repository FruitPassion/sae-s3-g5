from flask import Blueprint, render_template, flash, redirect, url_for

from custom_paquets.custom_form import RegisterPersonnelForm
from model.assister import getApprentisByFormation
from model.formation import getAllFormation
from model.personnel import checkPersonnel, checkPassword

auth = Blueprint('auth', __name__)


@auth.route('/')
def choix_connexion():
    return render_template('auth/index.html')


@auth.route('/connexion-personnel', methods=['GET', 'POST'])
def connexion_personnel():
    form = RegisterPersonnelForm()
    if form.validate_on_submit():
        if not checkPersonnel(form.login.data) or not checkPassword(form.login.data, form.password.data):
            flash('Compte inconnu ou mot de passe erroné.', 'error')
        else:
            return redirect(url_for('personnel.redirection_connexion'))
    return render_template('auth/connexion_personnel.html', form=form)


@auth.route('/choix-formation-apprentis', methods=['GET', 'POST'])
def choix_formation_apprentis():
    formations = getAllFormation()
    return render_template('auth/choix_formation_apprentis.html', formations=formations)


@auth.route('/choix-eleve-apprentis/<nom_formation>', methods=['GET', 'POST'])
def choix_eleve_apprentis(nom_formation):
    apprentis = getApprentisByFormation(nom_formation)
    return render_template('auth/choix_apprentis.html', apprentis=apprentis)


@auth.route('/connexion-apprentis/<login_apprenti>', methods=['GET', 'POST'])
def connexion_apprentis(login_apprenti):
    return "Hello World"


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return "Hello World"
