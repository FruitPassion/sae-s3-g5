from flask import url_for
from custom_paquets.converter import generate_login
from model.apprenti import Apprenti

'''
Test des controller du fichier api.py
'''


# Test de la vérification du mot de passe de l'apprenti
def test_api_check_password_apprenti(client, apprenti_mdp):
    # Data d'un apprenti existant
    data = {"login": apprenti_mdp.login,
            "password": apprenti_mdp.password}

    # Blocage d'un apprenti
    Apprenti.set_nbr_essais_connexion(apprenti_mdp.login, 5)
    response = client.post(url_for("api.api_check_password_apprenti"), json=data)

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification que l'apprenti est bloqué
    assert response.json["blocage"] == True

    # Test de déblocage d'un apprenti
    Apprenti.set_nbr_essais_connexion(apprenti_mdp.login, 0)
    response = client.post(url_for("api.api_check_password_apprenti"), json=data)

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification que l'apprenti n'est pas bloqué
    assert response.json["valide"] == True
    
    Apprenti.remove_apprenti(apprenti_mdp.id_apprenti)
    


# Test de la vérification du mot de passe de l'apprenti
def test_api_set_password_apprenti(client, apprenti_sans_mdp):
    # Data d'un apprenti inexistant
    data = {"login": generate_login("Mouline", "Jeanne"),
            "password": "222222"}
    
    # Ajout d'un mot de passe à un apprenti inexistant
    response = client.post(url_for("api.api_set_password_apprenti"),
                           json=data)
    
    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification que l'apprenti n'existe pas
    assert response.json["valide"] == False
    
    data = {"login": apprenti_sans_mdp.login,
            "password": apprenti_sans_mdp.password}
    
    # Ajout d'un mot de passe à un apprenti existant
    response = client.post(url_for("api.api_set_password_apprenti"),
                           json=data)
    
    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification que le mot de passe n'est encore pas défini
    assert response.json["valide"] == True
    
    # Ajout d'un mot de passe à un apprenti existant avec un mot de passe déjà défini
    response = client.post(url_for("api.api_set_password_apprenti"),
                           json=data)
    
    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification que le mot de passe n'est encore pas défini
    assert response.json["valide"] == False
    
    Apprenti.remove_apprenti(apprenti_sans_mdp.id_apprenti)
    

# Test des methodes de formation
def test_api_crud_formation(client, formation, gestion_connexion, personnel_super_admin, check_route_status):
    # Connexion en tant que super admin
    gestion_connexion.connexion_personnel_mdp(client, personnel_super_admin)
    
    # Partie archivage
    data = {"archive": True}

    # Test d'archivage d'une formation
    response = client.patch(url_for("api.api_archive_formation", id_formation=formation.id_formation), json=data)

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/formation/" + str(formation.id_formation))

    # Test de vérification de l'archivage
    assert response.json["valide"] == True
    
    data = {"archive": False}

    # Test de désarchivage
    response = client.patch(url_for("api.api_archive_formation", id_formation=formation.id_formation), json=data)

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/formation/" + str(formation.id_formation))

    # Test de vérification du désarchivage
    assert response.json["valide"] == True

    # Test de suppression
    response = client.delete(url_for("api.api_supprimer_formation",id_formation=formation.id_formation))

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/formation/" + str(formation.id_formation))

    # Test de vérification de la suppression
    assert response.json["valide"] == True
    


# Test des methodes de cours
def test_api_crud_cour(client, cour, gestion_connexion, personnel_super_admin, check_route_status):
    # Connexion en tant que super admin
    gestion_connexion.connexion_personnel_mdp(client, personnel_super_admin)
    
    # Partie archivage
    
    data = {"archive": True}

    # Test d'archivage d'une formation
    response = client.patch(url_for("api.api_archive_cours", id_cours=cour.id_cours), json=data)

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/cours/" + str(cour.id_cours))

    # Test de vérification de l'archivage
    assert response.json["valide"] == True
    
    data = {"archive": False}

    # Test de désarchivage
    response = client.patch(url_for("api.api_archive_cours", id_cours=cour.id_cours), json=data)

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/cours/" + str(cour.id_cours))

    # Test de vérification du désarchivage
    assert response.json["valide"] == True

    # Test de suppression
    response = client.delete(url_for("api.api_supprimer_cours",id_cours=cour.id_cours))

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/cours/" + str(cour.id_cours))

    # Test de vérification de la suppression
    assert response.json["valide"] == True



# Test de l'archivage d'un apprenti
def test_api_crud_apprenti(client, apprenti_mdp, gestion_connexion, personnel_super_admin, check_route_status):
    # Connexion en tant que super admin
    gestion_connexion.connexion_personnel_mdp(client, personnel_super_admin)
    
    # Partie archivage
    
    data = {"archive": True}

    # Test d'archivage d'un apprenti
    response = client.patch(url_for("api.api_archive_apprenti", id_apprenti=apprenti_mdp.id_apprenti),  json=data)

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/apprenti/" + str(apprenti_mdp.id_apprenti))

    # Test de vérification de l'archivage
    assert response.json["valide"] == True
    
    data = {"archive": False}

    # Test de désarchivage
    response = client.patch(url_for("api.api_archive_apprenti", id_apprenti=apprenti_mdp.id_apprenti),  json=data)

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/apprenti/" + str(apprenti_mdp.id_apprenti))

    # Test de vérification du désarchivage
    assert response.json["valide"] == True

    # Test de suppression
    response = client.delete(url_for("api.api_supprimer_apprenti", id_apprenti=apprenti_mdp.id_apprenti))

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/apprenti/" + str(apprenti_mdp.id_apprenti))
    
    # Test de vérification de la suppression
    assert response.json["valide"] == True


# Test de l'archivage d'un personnel
def test_api_crud_personnel(client, personnel_educateur, gestion_connexion, personnel_super_admin, check_route_status):
    # Connexion en tant que super admin
    gestion_connexion.connexion_personnel_mdp(client, personnel_super_admin)
    
    # Partie archivage
    data = {"archive": True}

    # Archivage d'un personnel
    response = client.patch(url_for("api.api_archive_personnel", id_personnel=personnel_educateur.id_personnel), json=data)
    
    check_route_status.check_both(response, 200, "/api/personnel/" + str(personnel_educateur.id_personnel))

    # Test de vérification de l'archivage
    assert response.json["valide"] == True
    
    data = {"archive": False}

    # Désarchivage d'un personnel
    response = client.patch(url_for("api.api_archive_personnel", id_personnel=personnel_educateur.id_personnel), json=data)
    
    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/personnel/" + str(personnel_educateur.id_personnel))

    # Test de vérification du désarchivage
    assert response.json["valide"] == True
    
    # Suppression d'un personnel
    response = client.delete(url_for("api.api_supprimer_personnel", id_personnel=personnel_educateur.id_personnel))
    
    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/api/personnel/" + str(personnel_educateur.id_personnel))

    # Test de vérification de la suppression
    assert response.json["valide"] == True


