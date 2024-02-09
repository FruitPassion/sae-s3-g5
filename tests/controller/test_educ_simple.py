from flask import url_for
from custom_paquets.tester_usages import connexion_personnel_pin

'''
Test des controller du fichier educateur_simple.py
'''

username = "MAC10"
passw = "101010"
formation = "Parcours plomberie"
apprenti = "ANG12"
fiche = 8
numero_fiche = 2

# Test de la route de redirection de connexion de l'éducateur simple
def test_redirection_connexion(client):
    connexion_personnel_pin(client, username, passw)

    response = client.get(url_for("personnel.choix_formation"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/personnel/choix-formation-personnel"


# Test de la route choix formation (affichage liste apprentis de cette formation)
def test_affichage_apprentis_formation(client):
    # Test connexion educateur simple
    connexion_personnel_pin(client, username, passw)
    response = client.get(url_for("personnel.choix_eleve", nom_formation=formation))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/personnel/choix-eleves/{formation}"


# Test de la route choix apprenti (affichage des fiches techniques de l'apprenti sélectionné)
def test_choix_apprenti(client):
    # Test connexion éducateur simple
    connexion_personnel_pin(client, username, passw)
    response = client.get(url_for("educ_simple.fiches_apprenti", apprenti=apprenti))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/educ-simple/{apprenti}/fiches"


# Test de la route commentaires (affichage des commentaires d'une fiche technique de l'apprenti sélectionné)
def test_lecture_commentaires(client):
    # Test connexion éducateur simple
    connexion_personnel_pin(client, username, passw)

    response = client.get(url_for("educ_simple.visualiser_commentaires", apprenti=apprenti, numero=numero_fiche))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/educ-simple/{apprenti}/{numero_fiche}/commentaires"


# Test de la route modification commentaire
def test_modification_commentaire(client):
    # Test connexion éducateur simple
    connexion_personnel_pin(client, username, passw)

    response = client.get(url_for("educ_simple.modifier_commentaires", apprenti=apprenti, numero=numero_fiche,
                                  type_commentaire="educateur"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/educ-simple/{apprenti}/{numero_fiche}/modifier-commentaires/educateur"

    response = client.get(url_for("educ_simple.modifier_commentaires", apprenti=apprenti, numero=numero_fiche,
                                  type_commentaire="apprenti"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/educ-simple/{apprenti}/{numero_fiche}/modifier-commentaires/apprenti"


# Tes de la route ajout commentaire
def test_ajouter_commentaire(client):
    # Test connexion éducateur simple
    connexion_personnel_pin(client, username, passw)
    response = client.get(url_for("educ_simple.ajouter_commentaires", apprenti=apprenti, numero=numero_fiche,
                                  type_commentaire="educateur"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/educ-simple/{apprenti}/{numero_fiche}/ajouter-commentaires/educateur"

    response = client.get(url_for("educ_simple.ajouter_commentaires", apprenti=apprenti, numero=numero_fiche,
                                  type_commentaire="apprenti"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/educ-simple/{apprenti}/{numero_fiche}/ajouter-commentaires/apprenti"

