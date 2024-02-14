import os
import sys
from configparser_crypt import ConfigParserCrypt

from custom_paquets.app_checker import lire_config
from custom_paquets.getion_logs import gestion_logs

import pymysql

pymysql.install_as_MySQLdb()

config = lire_config("config.txt")

if config == "prod":
    file = 'dbs.encrypted'
    conf_file = ConfigParserCrypt()
    try:
        with open('key.encrypt', 'rb') as passwd:
            password = passwd.read()
    except Exception as error:
        print("Fichier clée manquant")
        sys.exit(1)
    conf_file.aes_key = password
    conf_file.read_encrypted(file)
else:
    conf_file = {'DBS': {'db_password': 'password'}}



gestion_logs()


class DevConfig:
    """
    Configuration de l'application en mode développement
    """
    SECRET_KEY = "password"
    ENVIRONMENT = "development"
    FLASK_APP = "FichesDev"
    DEBUG = True
    SESSION_PERMANENT = False
    WTF_CSRF_ENABLED = False
    SESSION_TYPE = "filesystem"
    DB_SCHEMA = f"db_fiches_{config.lower()}"
    SQLALCHEMY_DATABASE_URI = f'mariadb://local_user:password@localhost:3306/{DB_SCHEMA}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REMEMBER_COOKIE_SAMESITE = "strict"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }


class ProdConfig:
    """
    Configuration de l'application en mode production
    """
    SECRET_KEY = os.urandom(32)
    ENVIRONMENT = "production"
    FLASK_APP = "FichesProd"
    WTF_CSRF_ENABLED = False
    DEBUG = False
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    DB_SCHEMA = f"db_fiches_{config.lower()}"
    SQLALCHEMY_DATABASE_URI = 'mariadb://user:{}@localhost:3306/{}'.format(
        conf_file['DBS']['db_password'], DB_SCHEMA)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REMEMBER_COOKIE_SAMESITE = "strict"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
