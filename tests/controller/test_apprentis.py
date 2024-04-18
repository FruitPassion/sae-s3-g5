from flask import url_for


'''
Test des controller du fichier apprentis.py
'''

NOM_FORMATION = "Parcours plomberie"
LOGIN = "DAJ12"

# Test de la route de redirection de connexion
def test_redirection_connexion(client, formation_fausse, apprenti_formation, gestion_connexion):
    # Connexion en tant qu'apprenti
    response = gestion_connexion.connexion_apprentis(client, formation_fausse, apprenti_formation)
    
    # Test d'accès à la route et redirection car formation non existante
    assert response.status_code == 404
    

# Test de la route de connexion
def test_connexion(client, formation, apprenti_formation, gestion_connexion):
    # Connexion en tant qu'apprenti
    response = gestion_connexion.connexion_apprentis(client, formation, apprenti_formation)
    
    # Test d'accès à la route et echech car non connecté
    assert response.status_code == 200
    
    
# Test de la route de suivi de progression
def test_suivi_progression(client, formation, apprenti_formation, gestion_connexion):
    # Connexion en tant qu'apprenti
    gestion_connexion.connexion_apprentis(client, formation, apprenti_formation)

    response = client.get(url_for("apprenti.suivi_progression"))

    assert response.status_code == 200
