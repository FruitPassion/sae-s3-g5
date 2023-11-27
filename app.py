import json

from flask_wtf import CSRFProtect
from werkzeug.exceptions import HTTPException

from controller.cip import cip
from controller.educateur_admin import educ_admin
from controller.educateur_simple import educ_simple
from custom_paquets import check_requirements
from custom_paquets.gestions_erreur import logging_erreur

check_requirements.checking()

import os
from flask import Flask, url_for, render_template

from controller.admin import admin
from controller.api import api
from controller.apprentis import apprenti
from controller.personnel import personnel
from controller.auth import auth

from model_db.shared_model import db

from pygit2 import Repository


class ProjectError(Exception):
    pass


class GitBranchError(ProjectError):
    pass


class ConfigurationError(ProjectError):
    pass


def create_app(config=None):
    if config not in [None, "Developpement"]:
        raise ConfigurationError("Configuration invalide")

    app = Flask(__name__, template_folder="view")

    if Repository('.').head.shorthand == "dev" or config == "Developpement":
        app.config.from_object('config.DevConfig')
    elif Repository('.').head.shorthand == "main":
        app.config.from_object('config.ProdConfig')
    else:
        raise GitBranchError("Branche inconnue")

    app.register_blueprint(auth)
    app.register_blueprint(api)
    app.register_blueprint(personnel)
    app.register_blueprint(apprenti)
    app.register_blueprint(admin)
    app.register_blueprint(cip)
    app.register_blueprint(educ_admin)
    app.register_blueprint(educ_simple)

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)

    """
    ERROR HANDLER
    """

    @app.errorhandler(Exception)
    def handle_error(e):
        logging_erreur(e)
        code = 500
        description = "Quelque chose s'est mal passé"
        gif = "sad_cat4.webp"
        author = "Santiago"
        if isinstance(e, HTTPException):
            code = e.code
            try:
                with open('static/error.json') as json_file:
                    errors = json.load(json_file)
                    description = errors[f"{code}"]["description"]
            except:
                pass
        return render_template("common/erreur.html", titre='erreur', erreur=f"Erreur {code}", description=description)

    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == "static":
            filename = values.get("filename", None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values["q"] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    return app


if __name__ == "__main__":
    create_app().run()
