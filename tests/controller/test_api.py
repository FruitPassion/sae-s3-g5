from flask import url_for
from custom_paquets.converter import generate_login
from custom_paquets.tester_usages import connexion_personnel_mdp
from model.formation import add_formation, get_formation_id
from model.personnel import get_id_personnel_by_login
from model.shared_model import Apprenti
from model.apprenti import add_apprenti, get_id_apprenti_by_login, set_nbr_essais_connexion

'''
Test des controller du fichier api.py
'''


# Test de la vérification du mot de passe de l'apprenti
def test_api_check_password_apprenti(client):
    # Set up d'un apprenti
    apprenti = Apprenti.query.filter_by(essaies=0).filter(Apprenti.login != 'dummy').first()
    mdp = "12369"

    # Blocage d'un apprenti
    set_nbr_essais_connexion(apprenti.login, 5)
    response = client.get(url_for("api.api_check_password_apprenti", user=apprenti.login, password=mdp))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification que l'apprenti est bloqué
    assert response.json["blocage"] == True

    # Test de déblocage d'un apprenti
    set_nbr_essais_connexion(apprenti.login, 0)
    response = client.get(url_for("api.api_check_password_apprenti", user=apprenti.login, password=mdp))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification que l'apprenti n'est pas bloqué
    assert response.json["valide"] == True


# Test de l'archivage d'une formation
def test_api_archiver_formation(client):
    # Partie archivage
    # Création d'une formation à archiver
    intitule = "Parcours électricité"
    niveau_qualification = 3
    groupe = "1"
    image = "null"

    add_formation(intitule, niveau_qualification, groupe, image, commit=False)

    # Set up d'une formation
    id_formation = get_formation_id(intitule)

    # Connexion en tant que superadmin
    superadmin = "JED10"
    mdp = "superadmin"
    connexion_personnel_mdp(client, superadmin, mdp)

    # Test d'archivage d'une formation
    response = client.get(url_for("api.api_archiver_formation", id_formation=id_formation))

    # Test d'accès à la route
    assert response.status_code == 200
    print(response.data)
    print(type(response))

    # Test de vérification de la route
    assert response.request.path == "/api/archiver-formation/" + str(id_formation)

    # Test de vérification de l'archivage
    assert response.json["valide"] == True

    # Test de désarchivage
    response = client.get(url_for("api.api_desarchiver_formation", id_formation=id_formation))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/api/desarchiver-formation/" + str(id_formation)

    # Test de vérification du désarchivage
    assert response.json["valide"] == True

    # Test de suppression
    response = client.get(url_for("api.api_supprimer_formation", id_formation=id_formation))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/api/supprimer-formation/" + str(id_formation)

    # Test de vérification de la suppression
    assert response.json["valide"] == True


# Test de l'archivage d'un apprenti
def test_archivage_apprenti(client):
    # Partie archivage
    # Création d'un apprenti à archiver
    nom = "SousFifre"
    prenom = "Malheureux"
    photo = "/url/photo.jpg"
    login = generate_login(nom, prenom)

    add_apprenti(nom, prenom, login, photo, commit=True)
    id_apprenti = get_id_apprenti_by_login(login)

    # Connexion en tant que superadmin
    superadmin = "JED10"
    mdp = "superadmin"
    connexion_personnel_mdp(client, superadmin, mdp)

    # Test d'archivage d'un apprenti
    response = client.get(url_for("api.api_archiver_apprenti", id_apprenti=id_apprenti))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/api/archiver-apprenti/" + str(id_apprenti)

    # Test de vérification de l'archivage
    assert response.json["valide"] == True

    # Test de désarchivage
    response = client.get(url_for("api.api_desarchiver_apprenti", id_apprenti=id_apprenti))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/api/desarchiver-apprenti/" + str(id_apprenti)

    # Test de vérification du désarchivage
    assert response.json["valide"] == True

    # Test de suppression
    response = client.get(url_for("api.api_supprimer_apprenti", id_apprenti=id_apprenti))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/api/supprimer-apprenti/" + str(id_apprenti)

    # Test de vérification de la suppression
    assert response.json["valide"] == True


# Test de l'archivage d'un personnel
def test_archivage_personnel(client):
    # Partie archivage
    # Récupération d'un personnel
    login = "ALL11"
    id_personnel = get_id_personnel_by_login(login)

    # Connexion en tant que superadmin
    superadmin = "JED10"
    mdp = "superadmin"
    connexion_personnel_mdp(client, superadmin, mdp)

    # Test d'archivage d'un personnel
    response = client.get(url_for("api.api_archiver_personnel", id_personnel=id_personnel))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/api/archiver-personnel/" + str(id_personnel)

    # Test de vérification de l'archivage
    assert response.json["valide"] == True

    # Test de désarchivage
    response = client.get(url_for("api.api_desarchiver_personnel", id_personnel=id_personnel))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/api/desarchiver-personnel/" + str(id_personnel)

    # Test de vérification du désarchivage
    assert response.json["valide"] == True
