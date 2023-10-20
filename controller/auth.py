from flask import Blueprint, render_template

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
    return "Hello World"


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return "Hello World"
