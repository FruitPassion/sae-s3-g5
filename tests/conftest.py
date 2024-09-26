import os
import sys

import pytest
from faker import Faker
from playwright.sync_api import Browser
from sqlalchemy import text

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app import create_app
from custom_paquets.converter import generate_login
from model.apprenti import Apprenti
from model.personnel import Personnel
from tests.utils import *

fake = Faker(["fr_FR"])


#####################################################
# Fixture pour la gestion de la base de données     #
#####################################################


@pytest.fixture(scope="session")
def creation(request):
    return request.param


@pytest.fixture(scope="session")
def browser(browser: Browser):
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def page(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    yield page


@pytest.fixture(scope="session")
def app(creation):
    app = create_app("test")

    with app.app_context():
        with open("./db_test.sql", "r") as file:
            sql_data = file.read().replace("\n", "")
            sql_data = sql_data.split("##")

        from model.shared_model import db

        with db.engine.connect() as conn:
            for data in sql_data:
                conn.execute(text(data))
            conn.execute(text("COMMIT;"))
            fichier = "test_data.json"
            create_or_delete_json(fichier)
            extract_from_classes(creation, fichier)

        yield app
    create_or_delete_json(fichier)


#####################################################
# Fixture pour la gestion des connexion             #
#####################################################


@pytest.fixture()
def gestion_connexion():
    class GestionConnexion:
        def connexion_personnel_mdp(self, client, personnel):
            Personnel.reset_nbr_essais_connexion(personnel.login)
            return client.post("/connexion-personnel-mdp", data=dict(login=personnel.login, password=personnel.password), follow_redirects=True)

        def connexion_personnel_pin(self, client, personnel, reset=True):
            if reset:
                Personnel.reset_nbr_essais_connexion(personnel.login)
            return client.post("/connexion-personnel-pin", data=dict(login_select=personnel.login, hiddencode=personnel.password), follow_redirects=True)

        def connexion_apprentis(self, client, formation, apprenti):
            Apprenti.reset_nbr_essais_connexion(apprenti["login"])
            return client.post(f"/connexion-apprentis/{formation['intitule']}/{apprenti['login']}", data=dict(login=apprenti["login"], password=apprenti["password"]), follow_redirects=True)

        def deconnexion(self, client):
            return client.get("/logout", follow_redirects=True)

    return GestionConnexion()


#####################################################
# Fixture pour test la route et le code de status   #
#####################################################


@pytest.fixture()
def check_route_status():
    """
    Test de vérification de la route et du code de status
    """

    class CheckRouteStatus:
        def check_both(self, response, status_code, path):
            assert response.status_code == status_code
            assert response.request.path == path

        def check_status(self, response, status_code):
            assert response.status_code == status_code

        def check_route(self, response, path):
            assert response.request.path == path

    return CheckRouteStatus()


@pytest.fixture()
def data_gen():
    return restitue_classes("test_data.json")
