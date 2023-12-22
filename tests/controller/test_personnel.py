from flask import url_for
from custom_paquets.tester_usages import connexion_personnel_pin
from model.formation import get_formation_id

'''
Test des controller du fichier personnel.py
'''

# identifiants de connexion pour les tests
username = "ALL11"
passw = "111111"
nom_formation = "Parcours maintenance batiment"
apprenti = "ANG12"


# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    connexion_personnel_pin(client, username, passw)

    response = client.get(url_for("personnel.choix_formation"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/personnel/choix-formation-personnel"


# Test de la route de choix des élèves
def test_choix_eleve(client):
    connexion_personnel_pin(client, username, passw)
    response = client.get(url_for("personnel.choix_eleve", nom_formation=nom_formation))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/personnel/choix-eleves/{nom_formation}"


# Test de la route du choix de la formation
def test_choix_formation(client):
    username = "JEO12"
    passw = "121212"
    connexion_personnel_pin(client, username, passw)

    nom_formation = "Parcours plomberie"
    response = client.get(url_for("personnel.choix_eleve", nom_formation=nom_formation))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/personnel/choix-eleves/" + nom_formation


# Test des routes de redirection de fiches apprentis
def test_redirection_fiches_apprentis(client):
    # Liste des identifiants de connexion
    liste_personnel = ["ALL11", "JEO12", "FAR16"]
    liste_mdp = ["111111", "121212", "161616"]

    # Test pour chaque personnel
    for i in range(3):
        connexion_personnel_pin(client, liste_personnel[i], liste_mdp[i])
        response = client.get(url_for("personnel.redirection_fiches", apprenti=apprenti))

        # Test d'accès à la route
        assert response.status_code == 302

        # Test de vérification de la route
        assert response.request.path == f"/personnel/redirection-fiches/{apprenti}"
