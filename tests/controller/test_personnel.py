import pytest


# test de la route de redirection de connexion
def test_redirection_connexion(client):
    response = client.get("/personnel/redirection-connexion")
    assert response.status_code == 200
    assert response.request.path == "/personnel/choix_formation.html"


# test de la route de personnalisation de la première page
def test_personnalisation(client):
    response = client.get("/personnel/personnalisation")
    assert response.status_code == 200
    assert response.request.path == "/personnel/personnaliser_fiche_texte_champs.html"


# test de la route de personnalisation de la deuxième page
def test_personnalisation_bis(client):
    response = client.get("/personnel/personnalisation-bis")
    assert response.status_code == 200
    assert response.request.path == "/personnel/personnaliser_fiche_couleur_fond.html"
