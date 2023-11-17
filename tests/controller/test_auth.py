from flask import url_for, session

from custom_paquets.tester_usages import connexion_personnel, deconnexion_personnel
from model.assister import get_apprentis_by_formation
from model.formation import get_all_formation


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
    response = client.get(url_for("auth.connexion_personnel"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/connexion-personnel"


def test_connexion_deconnexion(client):

    message_reussi = b'Connexion reussie'

    # Test connexion superadministrateur
    username = "JED10"
    passw = "superadmin"
    response = connexion_personnel(client, username, passw)
    with client.session_transaction() as sess:
        assert sess['name'] == 'JED10'
        assert sess['role'] == 'SuperAdministrateur'
    assert message_reussi in response.data

    # Test deconnexion
    response = deconnexion_personnel(client)
    with client.session_transaction() as sess:
        assert sess.get('name') is None
        assert sess.get('name') is None
    assert b'Deconnection reussie.' in response.data

    # Test connexion educateur admin
    username = "ALL11"
    passw = "educadmin"
    response = connexion_personnel(client, username, passw)
    with client.session_transaction() as sess:
        assert sess['name'] == 'ALL11'
        assert sess['role'] == 'Educateur Administrateur'
    assert message_reussi in response.data
    deconnexion_personnel(client)

    # Test connexion educateur
    username = "JEO12"
    passw = "educ"
    response = connexion_personnel(client, username, passw)
    with client.session_transaction() as sess:
        assert sess['name'] == 'JEO12'
        assert sess['role'] == 'Educateur'
    assert message_reussi in response.data
    deconnexion_personnel(client)

    # Test connexion cip
    username = "FAR16"
    passw = "cip"
    response = connexion_personnel(client, username, passw)
    with client.session_transaction() as sess:
        assert sess['name'] == 'FAR16'
        assert sess['role'] == 'CIP'
    assert message_reussi in response.data
    deconnexion_personnel(client)

    response = connexion_personnel(client, "12345", passw)
    assert b'Compte inconnu ou mot de passe invalide' in response.data

    response = connexion_personnel(client, username, f'{passw}x')
    assert b'Compte inconnu ou mot de passe invalide' in response.data


# Test de la route affichant la liste des formations
def test_choix_formation_apprentis(client):
    response = client.get(url_for("auth.choix_formation_apprentis"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/choix-formation-apprentis"

    # Test de verification de l'utilisation de tout les intitules de formation
    formations = get_all_formation()
    html = response.get_data(as_text=True)
    for formation in formations:
        assert 'class="boutton-formation">'+formation["intitule"] in html


# Test de la route affichant la liste des apprentis en fonction d'une formation
def test_choix_eleve_apprentis(client):
    nom_formation = "Agent de maintenance en bâtiment"
    response = client.get(url_for("auth.choix_eleve_apprentis", nom_formation=nom_formation))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/choix-eleve-apprentis/{nom_formation}"

    # Test de verification de l'utilisation de toutes les informations de l'apprentis
    apprentis = get_apprentis_by_formation(nom_formation)
    html = response.get_data(as_text=True)
    for apprenti in apprentis:
        assert 'class="libelle">'+apprenti["prenom"]+' '+apprenti["nom"] in html

