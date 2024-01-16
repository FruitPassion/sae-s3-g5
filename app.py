import logging

from custom_paquets import check_requirements
from custom_paquets.app_checker import check_git_branch

# Vérification de la présence des dépendances dans l'environnement virtuel
check_requirements.checking()

# Importation des librairies nécessaires
import json
import os

# Paquets flask
from flask import Flask, url_for, render_template
from flask_wtf import CSRFProtect
from werkzeug.exceptions import HTTPException

# Paquets git

# Paquet gestion d'erreur
from custom_paquets.gestions_erreur import logging_erreur, LogOpeningError

# model de la base de données
from model.shared_model import db

# Controller
from controller.cip import cip
from controller.educateur_admin import educ_admin
from controller.educateur_simple import educ_simple
from controller.admin import admin
from controller.api import api
from controller.apprentis import apprenti
from controller.personnel import personnel
from controller.auth import auth


# Fonction pour créer une application et la paramétrer
def create_app():
    # Déclaration de l'application
    # Changement du chemin d'accès des templates
    app = Flask(__name__, template_folder="view")

    # Remise à zéro du fichier de log
    if open('app.log', 'w').close():
        raise LogOpeningError("Impossible d'ouvrir le fichier de log")

    # Vérification de la branche du Git pour charger la bonne configuration
    # Utilisable uniquement dans la branche main ou dev
    check_git_branch(app)

    # Enregistrement des controller
    app.register_blueprint(auth)
    app.register_blueprint(api)
    app.register_blueprint(personnel)
    app.register_blueprint(apprenti)
    app.register_blueprint(admin)
    app.register_blueprint(cip)
    app.register_blueprint(educ_admin)
    app.register_blueprint(educ_simple)

    # Activation des Protections CRSF
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Initialisation du schema de la base de données dans l'application
    db.init_app(app)

    """
    ERROR HANDLER
    """

    # Gestion personnalisée des erreurs
    # 500 est l'erreur par défaut s'il n'y a pas de code disponible
    @app.errorhandler(Exception)
    def handle_error(e):
        description_plus = logging_erreur(e)
        code = 500
        description = "Quelque chose s'est mal passé"
        if isinstance(e, HTTPException):
            code = e.code
            try:
                with open('static/error.json') as json_file:
                    errors = json.load(json_file)
                    description = errors[f"{code}"]["description"]
            except SystemExit as e:
                logging.exception('error while accessing the dict')
                raise e
        return render_template("common/erreur.html", titre='erreur', erreur=f"Erreur {code}",
                               description=description, description_plus=description_plus), code

    # Permet d'horodater les fichiers utilisés dans le navigateur et d'éviter les problèmes de cache
    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    # Permet d'horodater les fichiers utilisés dans le navigateur et d'éviter les problèmes de cache
    def dated_url_for(endpoint, **values):
        if endpoint == "static":
            filename = values.get("filename", None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values["q"] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    # Renvoie l'application
    return app


# Appel principal pour lancer l'application
if __name__ == "__main__":
    create_app().run()
