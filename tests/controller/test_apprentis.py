from flask import url_for

from custom_paquets.tester_usages import connexion_apprentis

'''
Test des controller du fichier apprentis.py
'''

# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    
    nom_formation = "Parcours plomberie"
    login = "DAJ12"
    
    # Test de connexion bon mot de passe et bon login
    response = connexion_apprentis(client, nom_formation, login, '12369')
    
    # Test d'accès à la route et echech car non connecté
    assert response.status_code == 200
    
    
# Test de la route de suivi de progression
def test_suivi_progression(client):
    
    nom_formation = "Parcours plomberie"
    login = "DAJ12"
    
    # Connexion apprenti
    connexion_apprentis(client, nom_formation, login, '12369')
    
    response = client.get(url_for("apprenti.suivi_progression"))

    # Test d'accès à la route et echech car non connecté
    assert response.status_code == 200

    
# Test de la route de suivi de progression
def test_commentaires(client):
    
    nom_formation = "Parcours plomberie"
    login = "DAJ12"
    
    # Connexion apprenti
    connexion_apprentis(client, nom_formation, login, '12369')
    
    response = client.get(url_for("apprenti.suivi_progression", numero="2"))

    # Test d'accès à la route et echech car non connecté
    assert response.status_code == 200

    
# Test de la route de suivi de progression
def test_images(client):
    
    nom_formation = "Parcours plomberie"
    login = "DAJ12"
    
    # Connexion apprenti
    connexion_apprentis(client, nom_formation, login, '12369')
    
    response = client.get(url_for("apprenti.afficher_images", numero="2"))

    # Test d'accès à la route et echech car non connecté
    assert response.status_code == 200

    
# Test de la route de suivi de progression
def test_pdf(client):
    
    nom_formation = "Parcours plomberie"
    login = "DAJ12"
    
    # Connexion apprenti
    connexion_apprentis(client, nom_formation, login, '12369')
    
    response = client.get(url_for("apprenti.imprimer_pdf", numero="2"))

    # Test d'accès à la route et echech car non connecté
    assert response.status_code == 200