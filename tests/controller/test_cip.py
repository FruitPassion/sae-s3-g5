from flask import url_for

from custom_paquets.tester_usages import connexion_personnel

'''
Test des controller du fichier admin.py
'''


# Test de la route de redirection d'affichage des commentaires
def test_redirection_connexion(apprenti):
    # Test connexion superadministrateur
    username = "FAR10"
    passw = "cip"
    connexion_personnel(apprenti, username, passw)
    # identifiant de la fiche 1 d'apprenti
    id_fiche = 1

    response = apprenti.get(url_for("cip.afficher_commentaires"), apprenti = apprenti, idFiche = id_fiche)

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/cip/<apprenti>/<idFiche>/visualiser-commentaires"
