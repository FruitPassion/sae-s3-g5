import os
import sys

import pymysql
import redis
from configparser_crypt import ConfigParserCrypt

from custom_paquets.app_checker import lire_config
from custom_paquets.getion_logs import gestion_logs

pymysql.install_as_MySQLdb()

config = lire_config("config.txt")

if config == "prod":
    file = "dbs.encrypted"
    conf_file = ConfigParserCrypt()
    try:
        with open("key.encrypt", "rb") as passwd:
            password = passwd.read()
    except Exception as error:
        print("Fichier clée manquant")
        print(error)
        sys.exit(1)
    conf_file.aes_key = password
    conf_file.read_encrypted(file)
else:
    conf_file = {"DBS": {"db_password": "password"}}


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
    SESSION_TYPE = "filesystem"
    WTF_CSRF_ENABLED = False
    DB_SCHEMA = f"db_fiches_{config.lower()}"
    SQLALCHEMY_DATABASE_URI = f"mariadb://local_user:password@localhost:3306/{DB_SCHEMA}"
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
    WTF_CSRF_ENABLED = True
    DEBUG = False
    SESSION_PERMANENT = False
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    DB_SCHEMA = f"db_fiches_{config.lower()}"
    SQLALCHEMY_DATABASE_URI = "mariadb://user:{}@localhost:3306/{}".format(conf_file["DBS"]["db_password"], DB_SCHEMA)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REMEMBER_COOKIE_SAMESITE = "strict"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class TestConfig:
    """
    Configuration de l'application en mode test
    """

    SECRET_KEY = "password"
    ENVIRONMENT = "test"
    FLASK_APP = "FichesTest"
    WTF_CSRF_ENABLED = False
    DEBUG = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REMEMBER_COOKIE_SAMESITE = "strict"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
