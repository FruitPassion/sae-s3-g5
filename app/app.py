# Importation des librairies nécessaires
import os

from custom_paquets import check_requirements

check_requirements.checking()

from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

from custom_paquets import app_utils

from custom_paquets.gestions_erreur import LogOpeningError
from flask_session import Session
from dotenv import load_dotenv

load_dotenv()


# Fonction pour créer une application et la paramétrer
def create_app():
    from custom_paquets.app_checker import check_config

    config = os.getenv("CONFIG")
    check_config(config)

    # model de la base de données
    from model.shared_model import db

    # Déclaration de l'application
    # Changement du chemin d'accès des templates
    app = Flask(__name__, template_folder="view")

    # Remise à zéro du fichier de log
    if open("logs/error.log", "w").close():
        raise LogOpeningError("Impossible d'ouvrir le fichier de log")
    if open("logs/access.log", "w").close():
        raise LogOpeningError("Impossible d'ouvrir le fichier de log")

    app.config.from_object(f"config.{config.capitalize()}Config")

    # Importation des controller
    from controller.admin import admin
    from controller.api import api
    from controller.apprentis import apprenti
    from controller.auth import auth
    from controller.cip import cip
    from controller.educateur_admin import educ_admin
    from controller.educateur_simple import educ_simple
    from controller.personnel import personnel

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

    # Initialisation de la migration de la base de données
    Migrate(app, db)

    Session(app)

    # Redéfinition de la fonction url_for pour ajouter un timestamp
    app_utils.rewrite_url(app)

    # Gestion des erreurs sur l'application
    app_utils.error_handler(app, config)

    if config == "test":
        with app.app_context():
            db.create_all()

    # Renvoie l'application
    return app


# Appel principal pour lancer l'application
if __name__ == "__main__":
    create_app().run(host="0.0.0.0")
