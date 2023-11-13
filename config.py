import os

import pymysql

pymysql.install_as_MySQLdb()


class DevConfig:
    SECRET_KEY = "3@$=)+Nj{HlH8E&u-43}K.~)C3JTSCL5L9a63_iH#UN6V4nd9d"
    ENVIRONMENT = "development"
    FLASK_APP = "FichesDev"
    DEBUG = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_DATABASE_URI = 'mariadb://local_user:password@localhost:3306/db_fiches_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig:
    SECRET_KEY = os.urandom(32)
    ENVIRONMENT = "production"
    FLASK_APP = "FichesProd"
    DEBUG = False
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_DATABASE_URI = 'mariadb://local_user:password@localhost:3306/db_fiches_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
