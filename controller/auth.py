from flask import Blueprint, render_template

from custom_paquets.custom_form import RegisterPersonnelForm
from model.personnel import getAllPersonnel

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def choix_connexion():
    return "Hello World"


@auth.route('/choix-formation', methods=['GET', 'POST'])
def choix_formation_apprentis():
    return "Hello world"


@auth.route('/choix-eleve', methods=['GET', 'POST'])
def choix_eleve_apprentis():
    return "Hello world"


@auth.route('/connexion-apprentis', methods=['GET', 'POST'])
def connexion_apprentis():
    return "Hello World"


@auth.route('/connexion-personnel', methods=['GET', 'POST'])
def connexion_personnel():
    form = RegisterPersonnelForm()
    if form.validate_on_submit():
        return "connecté"
    return render_template('auth/connexion_personnel.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return "Hello World"
