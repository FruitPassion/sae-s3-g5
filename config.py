import os
import logging

import pymysql

pymysql.install_as_MySQLdb()


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_NAME = ''
LOG_FILE_INFO = 'logs/access.log'
LOG_FILE_ERROR = 'logs/error.log'
log = logging.getLogger(LOG_NAME)
log_formatter = logging.Formatter(LOG_FORMAT)

# comment this to suppress console output
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
log.addHandler(stream_handler)

file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='a')
file_handler_info.setFormatter(log_formatter)
file_handler_info.setLevel(logging.INFO)
log.addHandler(file_handler_info)

file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='a')
file_handler_error.setFormatter(log_formatter)
file_handler_error.setLevel(logging.ERROR)
log.addHandler(file_handler_error)

log.setLevel(logging.INFO)


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
