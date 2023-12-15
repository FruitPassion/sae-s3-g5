from flask import url_for
from custom_paquets.tester_usages import connexion_personnel

'''
Test des controller du fichier admin.py
'''


# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    # Test connexion superadministrateur
    username = "JED10"
    passw = "superadmin"
    connexion_personnel(client, username, passw)

    response = client.get(url_for("admin.accueil_admin"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/accueil-admin"


# Test de la route de redirection de la gestion des formations
def test_redirection_gestion_formation(client):
    response = client.get(url_for("admin.gestion_formation"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/gestion-formation"


# Test de la route de redirection de la gestion des apprentis
def test_redirection_gestion_apprentis(client):
    response = client.get(url_for("admin.gestion_apprenti"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/gestion-apprenti"


# Test de la route de redirection de la gestion du personnel
def test_redirection_gestion_personnel(client):
    response = client.get(url_for("admin.gestion_personnel"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/gestion-personnel"