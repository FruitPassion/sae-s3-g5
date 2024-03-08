

import json
import logging
import os
from flask import render_template, url_for
from custom_paquets.gestions_erreur import logging_erreur, LogOpeningError
from werkzeug.exceptions import HTTPException


def rewrite_url(app):
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
    
def error_handler(app, config):
    @app.errorhandler(Exception)
    def handle_error(e):
        description_plus = logging_erreur(e)
        code = 500
        description = "Quelque chose s'est mal passé"
        if isinstance(e, HTTPException):
            code = e.code
            try:
                with open('static/error.json', encoding="utf-8") as json_file:
                    errors = json.load(json_file)
                    description = errors[f"{code}"]["description"]
            except SystemExit as e:
                logging.exception('Erreur lors de la lecture du fichier error.json')
                raise e
        return render_template("common/erreur.html", titre='erreur', erreur=f"Erreur {code}",
                               description=description, description_plus=description_plus,
                               config=config), code