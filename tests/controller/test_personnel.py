from flask import url_for

'''
Test des controller du fichier auth.py
'''


# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    response = client.get(url_for("personnel.redirection_connexion"))

    # Test d'accès à la route
    assert response.status_code == 200

    assert response.request.path == "/personnel/redirection-connexion"


# Test de la route de personnalisation de la première page
def test_personnalisation(client):
    response = client.get(url_for("personnel.personnalisation"))

    # Test d'accès à la route
    assert response.status_code == 200
    assert response.request.path == "/personnel/personnalisation"


# Test de la route de personnalisation de la deuxième page
def test_personnalisation_bis(client):
    response = client.get(url_for("personnel.personnalisation_bis"))

    # Test d'accès à la route
    assert response.status_code == 200
    assert response.request.path == "/personnel/personnalisation-bis"
