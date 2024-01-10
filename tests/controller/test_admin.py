from flask import url_for
from custom_paquets.tester_usages import connexion_personnel_mdp

'''
Test des controller du fichier admin.py
'''


# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    # Test connexion superadministrateur
    username = "JED10"
    passw = "superadmin"
    connexion_personnel_mdp(client, username, passw)

    response = client.get(url_for("admin.accueil_admin"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/admin/accueil-admin"


# Test de la route de redirection de la gestion des formations
def test_redirection_gestion_formations(client):
    response = client.get(url_for("admin.gestion_formations"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/gestion-formations"


# Test de la route de redirection de la gestion des apprentis
def test_redirection_gestion_apprentis(client):
    response = client.get(url_for("admin.gestion_apprentis"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/gestion-apprentis"


# Test de la route de redirection de la gestion du personnel
def test_redirection_gestion_personnel(client):
    response = client.get(url_for("admin.gestion_personnel"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/gestion-personnel"