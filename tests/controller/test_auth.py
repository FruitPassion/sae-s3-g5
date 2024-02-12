from flask import url_for

from custom_paquets.tester_usages import connexion_apprentis, connexion_personnel_pin, connexion_personnel_mdp, deconnexion
from model.cours import Cours
from model.formation import Formation

'''
Test des controller du fichier auth.py
'''

COMPTE_INC_OU_INV = b'Compte inconnu ou mot de passe invalide'

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


def test_connexion_deconnexion_personnel(client):

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
    response = deconnexion(client)
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
    deconnexion(client)

    # Test connexion educateur
    username = "MAC10"
    passw = "101010"
    response = connexion_personnel_pin(client, username, passw)
    with client.session_transaction() as sess:
        assert sess['name'] == 'MAC10'
        assert sess['role'] == 'Educateur'
    assert response.status_code == 200
    assert response.request.path == "/personnel/choix-formation-personnel"
    deconnexion(client)

    # Test connexion cip
    username = "FAR16"
    passw = "161616"
    response = connexion_personnel_pin(client, username, passw)
    
    with client.session_transaction() as sess:
        assert sess['name'] == 'FAR16'
        assert sess['role'] == 'CIP'
    assert response.status_code == 200
    assert response.request.path == "/personnel/choix-formation-personnel"
    deconnexion(client)

    response = connexion_personnel_pin(client, "JED10", '123456')

    assert COMPTE_INC_OU_INV in response.data


# Test de la route affichant la liste des formations
def test_choix_formation_apprentis(client):
    response = client.get(url_for("auth.choix_formation_apprentis"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/choix-formation-apprentis"

    # Test de verification de l'utilisation de tout les intitules de formation
    formations = Formation.get_all_formations()
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
    apprentis = Cours.get_apprentis_by_formation(nom_formation)
    html = response.get_data(as_text=True)
    for apprenti in apprentis:
        assert 'class="libelle">' + apprenti.prenom + ' ' + apprenti.nom in html

    nom_formation = "Page erreur"
    response = client.get(url_for("auth.choix_eleve_apprentis", nom_formation=nom_formation))

    # Test d'accès à la route
    assert response.status_code == 404


def test_connexion_deconnexion_apprenti(client):
    # Test accès apprenti sans login
    response = client.get(url_for("apprenti.redirection_connexion"))

    # Test d'accès à la route et echec car non connecté
    assert response.status_code == 302
    
    nom_formation = "Parcours plomberie"
    login = "DAJ12"
    
    # Test de connexion bon mot de passe et bon login
    response = connexion_apprentis(client, nom_formation, login, '12369')
    assert response.status_code == 200
    assert response.request.path == "/apprenti/redirection-connexion"
    
    with client.session_transaction() as sess:
        assert sess['name'] == 'DAJ12'
        assert sess['role'] == 'apprentis'
        
    # Test deconnexion
    response = deconnexion(client)
    with client.session_transaction() as sess:
        assert sess.get('name') is None
    assert response.status_code == 200
    assert response.request.path == "/"
        
    # Test de connexion mauvais login
    response = connexion_apprentis(client, nom_formation, 'BEN10', '12367')
    
    assert COMPTE_INC_OU_INV in response.data
    
    
    # Test de connexion mauvais mot de passe et bon login
    response = connexion_apprentis(client, nom_formation, login, '12367')
    
    assert COMPTE_INC_OU_INV in response.data
    