import os
import logging

import pymysql

pymysql.install_as_MySQLdb()

# Configuration du logger
logging.basicConfig(level=logging.ERROR,
                    filename='app.log',
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class DevConfig:
    """
    Configuration de l'application en mode développement
    """
    SECRET_KEY = "3@$=)+Nj{HlH8E&u-43}K.~)C3JTSCL5L9a63_iH#UN6V4nd9d"
    ENVIRONMENT = "development"
    FLASK_APP = "FichesDev"
    DEBUG = True
    SESSION_PERMANENT = False
    WTF_CSRF_ENABLED = False
    SESSION_TYPE = "filesystem"
    DB_SCHEMA = "db_fiches_dev"
    SQLALCHEMY_DATABASE_URI = f'mariadb://local_user:password@localhost:3306/{DB_SCHEMA}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REMEMBER_COOKIE_SAMESITE = "strict"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class MainConfig:
    """
    Configuration de l'application en mode production
    """
    SECRET_KEY = os.urandom(32)
    ENVIRONMENT = "production"
    FLASK_APP = "FichesProd"
    WTF_CSRF_ENABLED = True
    DEBUG = False
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    DB_SCHEMA = "db_fiches_prod"
    SQLALCHEMY_DATABASE_URI = f'mariadb://local_user:password@localhost:3306/{DB_SCHEMA}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REMEMBER_COOKIE_SAMESITE = "strict"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
