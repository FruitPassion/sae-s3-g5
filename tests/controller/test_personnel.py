from flask import url_for
from custom_paquets.tester_usages import connexion_personnel
from model.formation import get_formation_id

'''
Test des controller du fichier personnel.py
'''

# identifiants de connexion pour les tests
username = "ALL11"
# passw = "educadmin"
passw = "111111" 
nom_formation = "Parcours maintenance batiment"
apprenti = "ANG12"


# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    connexion_personnel(client, username, passw)

    response = client.get(url_for("personnel.choix_formation"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/personnel/choix-formation-personnel"


# Test de la route de choix des élèves
def test_choix_eleve(client):
    connexion_personnel(client, username, passw)
    response = client.get(url_for("personnel.choix_eleve", nom_formation=nom_formation))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/personnel/choix-eleves/{nom_formation}"

"""
# Test de la route de personnalisation de la première page
def test_personnalisation(client):
    
    connexion_personnel(client,username,passw)
    response = client.get(url_for("personnel.personnalisation"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/personnel/personnalisation"

    # Test de la page HTML
    html = response.get_data(as_text=True)
    print(html)
    # Vérification des labels dans la page
    listefor = ['"selecteur_police"', '"taille_police"', '"selecteur_type_champ"', '"selecteur_niveau"', '"selecteur_pictogramme"']
    for name in listefor:
        assert 'for=' + name in html

    # vérification des ids dans la page
    listeids = ['"zone_texte"', '"selecteur_police"', '"taille_police"', '"visualisation"', '"color_picker"',
                '"visualisation_texte"', '"texte_visualisation"', '"zone_champs"', '"selecteur_type_champ"',
                '"selecteur_niveau"', '"selecteur_pictogramme"']
    for name in listeids:
        assert 'id=' + name in html


# Test de la route de personnalisation de la deuxième page
def test_personnalisation_bis(client):
    connexion_personnel(client,username,passw)

    response = client.get(url_for("personnel.personnalisation_bis"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/personnel/personnalisation-bis"

    # Test de la page HTML
    html = response.get_data(as_text=True)
    # Vérification des ids dans la page
    listeids = ['"couleur"', '"color_picker"', '"couleur_fond"']
    for name in listeids:
        assert 'id=' + name in html
"""

# Test de la route du choix de la formation
def test_choix_formation(client):
    username = "JEO12"
    passw = "educ"
    connexion_personnel(client, username, passw)

    nom_formation = "Parcours plomberie"
    response = client.get(url_for("personnel.choix_eleve", nom_formation=nom_formation))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/personnel/choix-eleves/"+nom_formation


# Test des routes de redirection de fiches apprentis
def test_redirection_fiches_apprentis(client):
    # Liste des identifiants de connexion
    liste_personnel = ["ALL11", "JEO12", "FAR16"]
    liste_mdp = ["111111", "121212", "161616"]

    # Test pour chaque personnel
    for i in range(3):
        connexion_personnel(client,liste_personnel[i],liste_mdp[i])
        response = client.get(url_for("personnel.redirection_fiches", apprenti=apprenti))

        # Test d'accès à la route
        assert response.status_code == 302

        # Test de vérification de la route
        assert response.request.path == f"/personnel/redirection-fiches/{apprenti}"

