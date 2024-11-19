import os

import redis
from custom_paquets.getion_logs import gestion_logs
from dotenv import load_dotenv

load_dotenv()

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
    DB_SCHEMA = "main"
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
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
    SESSION_REDIS = redis.from_url(f"redis://{os.getenv('CACHE_HOST')}:6379")
    DB_SCHEMA = "main"
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
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
