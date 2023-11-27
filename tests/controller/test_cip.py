from flask import url_for

from custom_paquets.tester_usages import connexion_personnel

'''
Test des controller du fichier admin.py
'''


# Test de la route de redirection d'affichage des commentaires
def test_redirection_connexion(client):
    # Test connexion superadministrateur
    username = "FAR16"
    passw = "cip"
    connexion_personnel(client, username, passw)
    # identifiant de la fiche 1 d'apprenti
    id_fiche = 1
    # login d'un apprenti pour le test
    apprenti = "DAJ12"

    # A MODIFIER (Miri)
    response = client.get(url_for("cip.visualiser_commentaires", apprenti = apprenti, idFiche = id_fiche))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    # A MODIFIER (Miri)
    assert response.request.path == "/cip/<apprenti>/<idFiche>/visualiser-commentaires"
