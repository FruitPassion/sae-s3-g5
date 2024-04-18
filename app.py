# Importation des librairies nécessaires
import os
import sys

# Vérification de la présence des dépendances dans l'environnement virtuel
from custom_paquets import check_requirements
check_requirements.checking()

# Paquets flask
from flask import Flask, url_for, render_template
from flask_wtf import CSRFProtect
from flask_session import Session
from werkzeug.exceptions import HTTPException
from custom_paquets import app_utils

# Paquet gestion d'erreur
from custom_paquets.gestions_erreur import LogOpeningError


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
    
    Session(app)

    # Redéfinition de la fonction url_for pour ajouter un timestamp
    app_utils.rewrite_url(app)
    
    # Gestion des erreurs sur l'application
    app_utils.error_handler(app, config)
    
    if config == 'test':
        with app.app_context():
            db.create_all()
            

    # Renvoie l'application
    return app


# Appel principal pour lancer l'application
if __name__ == "__main__":
    try:
        create_app(sys.argv[1]).run(host="0.0.0.0")
    except IndexError:
        raise ValueError("Argument de lancement manquant (dev, test ou prod)")
