from flask import url_for

from custom_paquets.tester_usages import connexion_personnel_pin, connexion_personnel_mdp, deconnexion_personnel
from model.cours import get_apprentis_by_formation
from model.formation import get_all_formations

'''
Test des controller du fichier auth.py
'''


# Tests de la route d'accueil du site
def test_choix_connexion(client):
    response = client.get(url_for("auth.choix_connexion"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/"


# Tests de la route de connexion pour le personnel avant l'identification
def test_connexion_personnel_chargement(client):
    # Version PIN
    response = client.get(url_for("auth.connexion_personnel_pin"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/connexion-personnel-pin"

    # Version MDP
    response = client.get(url_for("auth.connexion_personnel_mdp"))
    assert response.status_code == 200
    assert response.request.path == "/connexion-personnel-mdp"


def test_connexion_deconnexion(client):

    # Test connexion superadministrateur
    username = "JED10"
    passw = "superadmin"
    response = connexion_personnel_mdp(client, username, passw)
    with client.session_transaction() as sess:
        assert sess['name'] == 'JED10'
        assert sess['role'] == 'SuperAdministrateur'

    assert response.status_code == 200
    assert response.request.path == "/admin/accueil-admin"

    # Test deconnexion
    response = deconnexion_personnel(client)
    with client.session_transaction() as sess:
        assert sess.get('name') is None
    assert response.status_code == 200
    assert response.request.path == "/"

    # Test connexion educateur admin
    username = "ALL11"
    passw = "111111"
    response = connexion_personnel_pin(client, username, passw)
    with client.session_transaction() as sess:
        assert sess['name'] == 'ALL11'
        assert sess['role'] == 'Educateur Administrateur'

    assert response.status_code == 200
    assert response.request.path == "/educ-admin/accueil-educadmin"
    deconnexion_personnel(client)

    # Test connexion educateur
    username = "MAC10"
    passw = "101010"
    response = connexion_personnel_pin(client, username, passw)
    with client.session_transaction() as sess:
        assert sess['name'] == 'MAC10'
        assert sess['role'] == 'Educateur'
    assert response.status_code == 200
    assert response.request.path == "/personnel/choix-formation-personnel"
    deconnexion_personnel(client)

    # Test connexion cip
    username = "FAR16"
    passw = "161616"
    response = connexion_personnel_pin(client, username, passw)
    print(response.data)
    with client.session_transaction() as sess:
        assert sess['name'] == 'FAR16'
        assert sess['role'] == 'CIP'
    assert response.status_code == 200
    assert response.request.path == "/personnel/choix-formation-personnel"
    deconnexion_personnel(client)

    response = connexion_personnel_pin(client, "JED10", '123456')
    print(response.data)
    assert b'Compte inconnu ou mot de passe invalide' in response.data


# Test de la route affichant la liste des formations
def test_choix_formation_apprentis(client):
    response = client.get(url_for("auth.choix_formation_apprentis"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/choix-formation-apprentis"

    # Test de verification de l'utilisation de tout les intitules de formation
    formations = get_all_formations()
    html = response.get_data(as_text=True)
    for formation in formations:
        assert formation.intitule in html


# Test de la route affichant la liste des apprentis en fonction d'une formation
def test_choix_eleve_apprentis(client):
    nom_formation = "Parcours maintenance batiment"
    response = client.get(url_for("auth.choix_eleve_apprentis", nom_formation=nom_formation))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/choix-eleve-apprentis/{nom_formation}"

    # Test de verification de l'utilisation de toutes les informations de l'apprentis
    apprentis = get_apprentis_by_formation(nom_formation)
    html = response.get_data(as_text=True)
    for apprenti in apprentis:
        assert 'class="libelle">' + apprenti.prenom + ' ' + apprenti.nom in html

    nom_formation = "Page erreur"
    response = client.get(url_for("auth.choix_eleve_apprentis", nom_formation=nom_formation))

    # Test d'accès à la route
    assert response.status_code == 404
