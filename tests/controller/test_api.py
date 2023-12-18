from flask import url_for
from model.formation import add_formation, get_formation_id
from model_db.shared_model import db, Apprenti
from model.apprenti import update_nbr_essaies_connexion

'''
Test des controller du fichier api.py
'''


# Test de la vérification du mot de passe de l'apprenti
def test_api_check_password_apprenti(client):
    # Set up d'un apprenti
    apprenti = Apprenti.query.filter_by(essaies=0).filter(Apprenti.login != 'dummy').first()
    mdp = "12369"

    # Blocage d'un apprenti
    update_nbr_essaies_connexion(apprenti.login, 5)
    response = client.get(url_for("api.api_check_password_apprenti", user=apprenti.login, password=mdp))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification que l'apprenti est bloqué
    assert response.json["blocage"] == True

    # Test de déblocage d'un apprenti
    update_nbr_essaies_connexion(apprenti.login, 0)
    response = client.get(url_for("api.api_check_password_apprenti", user=apprenti.login, password=mdp))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification que l'apprenti n'est pas bloqué
    assert response.json["valide"] == True


# Test de l'archivage d'une formation
def test_api_archiver_formation(client):
    # Création d'une formation à archiver
    intitule = "Parcours électricité"
    niveau_qualification = 3
    groupe = "1"
    image = "formation_image/elec.jpg"

    add_formation(intitule, niveau_qualification, groupe, image, commit=False)

    # Set up d'une formation
    id_formation = get_formation_id(intitule)

    # Test d'archivage d'une formation
    response = client.get(url_for("api.api_archiver_formation", id_formation=id_formation))

    # Test d'accès à la route
    assert response.status_code == 302
    print(response.data)
    print(type(response))
    # Test de vérification de l'archivage
    assert response.json["valide"] == True
