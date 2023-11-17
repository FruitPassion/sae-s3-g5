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
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/admin/accueil-admin"
