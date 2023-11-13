from flask import url_for

'''
Test des controller du fichier admin.py
'''

# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    response = client.get(url_for("admin.redirection_connexion"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test dde vérification de la route
    assert response.request.path == "/admin/redirection-connexion"