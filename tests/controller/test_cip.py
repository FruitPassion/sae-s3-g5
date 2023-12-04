from flask import url_for

from custom_paquets.tester_usages import connexion_personnel

'''
Test des controller du fichier cip.py
'''

username = "FAR16"
passw = "cip"
formation = "Parcours plomberie"
apprenti = "DAJ12"

# Test de la route de redirection de connexion de la CIP
def test_redirection_connexion(client):
    connexion_personnel(client, username, passw)
    response = client.get(url_for("personnel.choix_formation"))
    
    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/personnel/choix-formation-personnel"


# Test de la route choix formation (affichage liste apprentis de cette formation)
def test_affichage_apprentis_formation(client):
    # Test connexion CIP
    connexion_personnel(client, username, passw)
    response = client.get(url_for("personnel.choix_eleve", nom_formation = formation))

    # Test d'accès à la route
    assert response.status_code == 302
    
    # Test de vérification de la route
    assert response.request.path == f"/personnel/choix-eleves/{formation}"


# Test de la route choix apprenti (affichage des opérations possibles pour la CIP)
def test_choix_apprenti(client):
    # Test connexion CIP
    connexion_personnel(client, username, passw)
    response = client.get(url_for("cip.affiche_choix", apprenti = apprenti))

    # Test d'accès à la route
    assert response.status_code == 302
    
    # Test de vérification de la route
    assert response.request.path == f"/cip/{apprenti}/choix-operations"


# Test de la route choix fiche apprenti (affichage des fiches techniques de DAJ12)
def test_choix_fiche(client):
    # Test connexion CIP
    connexion_personnel(client, username, passw)
    response = client.get(url_for("cip.fiches_apprenti", apprenti = apprenti))

    # Test d'accès à la route
    assert response.status_code == 302
    
    # Test de vérification de la route
    assert response.request.path == f"/cip/{apprenti}/fiches"

"""
A VALIDER UNE FOIS QUE LE SUIVI DE PROGRESSION SERA FAIT

# Test de la route suivi de progression de l'apprenti 
def test_suivi_progression(client):
    # Test connexion CIP
    connexion_personnel(client, username, passw)
    response = client.get(url_for("cip.suivi_progression_apprenti", apprenti = apprenti))

    # Test d'accès à la route
    assert response.status_code == 302
    
    # Test de vérification de la route
    assert response.request.path == f"/cip/{apprenti}/suivi-progression"
"""

"""
A VALIDER UNE FOIS QUE L'ADAPTATION EN SITUATION D'EXAMEN SERA FAIT

# Test de la route de l'adaptation en situation d'examen de l'apprenti 
def test_adaptation_situation_exam(client):
    # Test connexion CIP
    connexion_personnel(client, username, passw)
    response = client.get(url_for("cip.suivi_progression_apprenti", apprenti = apprenti))

    # Test d'accès à la route
    assert response.status_code == 302
    
    # Test de vérification de la route
    assert response.request.path == f"/cip/{apprenti}/adaptation-situation-examen"
"""

# Test de la route de redirection d'affichage des commentaires
def test_redirection_commentaires(client):
    # Test connexion CIP
    connexion_personnel(client, username, passw)

    # identifiant de la fiche 1 d'apprenti
    id_fiche = 7

    # A MODIFIER (Miri)
    response = client.get(url_for("cip.visualiser_commentaires", apprenti = apprenti, fiche = id_fiche))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    # A MODIFIER (Miri)
    assert response.request.path == f"/cip/{apprenti}/{id_fiche}/commentaires"
