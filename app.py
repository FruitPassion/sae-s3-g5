from flask_wtf import CSRFProtect

from custom_paquets import check_requirements

check_requirements.checking()

import os
from flask import Flask, url_for

from controller.admin import admin
from controller.api import api
from controller.apprentis import apprenti
from controller.personnel import personnel
from controller.auth import auth

from model_db.shared_model import db

from pygit2 import Repository





def create_app(config=None):
    if config not in [None, "Developpement"]:
        raise Exception("Configuration invalide")

    app = Flask(__name__, template_folder="view")

    if Repository('.').head.shorthand == "dev" or config == "Developpement":
        app.config.from_object('config.DevConfig')
    elif Repository('.').head.shorthand == "main":
        app.config.from_object('config.ProdConfig')
    else:
        raise Exception("Branche inconnue")

    app.register_blueprint(auth)
    app.register_blueprint(api)
    app.register_blueprint(personnel)
    app.register_blueprint(apprenti)
    app.register_blueprint(admin)

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)

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
