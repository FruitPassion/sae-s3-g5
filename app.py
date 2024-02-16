# Importation des librairies nécessaires
import json
import os
import logging
import sys

# Vérification de la présence des dépendances dans l'environnement virtuel
from custom_paquets import check_requirements
check_requirements.checking()

# Paquets flask
from flask import Flask, url_for, render_template
from flask_wtf import CSRFProtect
from werkzeug.exceptions import HTTPException

# Paquet gestion d'erreur
from custom_paquets.gestions_erreur import logging_erreur, LogOpeningError


# Fonction pour créer une application et la paramétrer
def create_app(config=None):
    from custom_paquets.app_checker import check_config, lire_config
    
    # Vérification de la configuration demandée.
    # Si aucune configuration n'est demandée, le programme s'arrête
    check_config(config)
    if not os.path.exists('config.txt'):
        file = open('config.txt', 'w')
        file.close()
    with open("config.txt", "w") as file:
        file.write(config)
        
    config = lire_config("config.txt")
    
    # model de la base de données
    from model.shared_model import db
    
    # Déclaration de l'application
    # Changement du chemin d'accès des templates
    app = Flask(__name__, template_folder="view")

    # Remise à zéro du fichier de log
    if open('logs/error.log', 'w').close():
        raise LogOpeningError("Impossible d'ouvrir le fichier de log")
    if open('logs/access.log', 'w').close():
        raise LogOpeningError("Impossible d'ouvrir le fichier de log")

    # Chargement de la configuration dev ou prod
    app.config.from_object(f"config.{config.capitalize()}Config")
    
    
    # Importation des controller
    from controller.cip import cip
    from controller.educateur_admin import educ_admin
    from controller.educateur_simple import educ_simple
    from controller.admin import admin
    from controller.api import api
    from controller.apprentis import apprenti
    from controller.personnel import personnel
    from controller.auth import auth

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
                with open('static/error.json', encoding="utf-8") as json_file:
                    errors = json.load(json_file)
                    description = errors[f"{code}"]["description"]
            except SystemExit as e:
                logging.exception('Erreur lors de la lecture du fichier error.json')
                raise e
        return render_template("common/erreur.html", titre='erreur', erreur=f"Erreur {code}",
                               description=description, description_plus=description_plus,
                               config=config), code

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
    try:
        create_app(sys.argv[1]).run(host="0.0.0.0")
    except IndexError:
        raise ValueError("Argument de lancement manquant (dev ou prod)")
