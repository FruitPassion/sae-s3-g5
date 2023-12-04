from flask import url_for
from custom_paquets.tester_usages import connexion_personnel
from model.formation import get_formation_id

'''
Test des controller du fichier educateur_simple.py
'''

# identifiants de connexion pour les tests
username = "MAC1010"
passw = "101010"
nom_formation = "Parcours maintenance batiment"
apprenti = "ANG12"

# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    connexion_personnel(client, username, passw)

    response = client.get(url_for("educ_simple.fiches_apprenti", apprenti=apprenti))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/educ-simple/{ apprenti }/fiches"