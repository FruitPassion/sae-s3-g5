from flask import url_for

'''
Test des controller du fichier auth.py
'''


def test_auth_index(client):
    response = client.get(url_for("auth.choix_connexion"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de récuperation d'une string dans le fichier HTML
    assert b'<label id="labelProf">Educateur</label>' in response.data
