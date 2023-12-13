from flask import url_for

'''
Test des controller du fichier apprentis.py
'''

# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    response = client.get(url_for("apprenti.redirection_connexion"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test dde vérification de la route
    assert response.request.path == "/apprenti/redirection-connexion"
    
# Test de la route de suivi de progression
def test_suivi_progression(client):
    response = client.get(url_for("apprenti.suivi_progression"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test dde vérification de la route
    assert response.request.path == "/apprenti/redirection-connexion/suivi"