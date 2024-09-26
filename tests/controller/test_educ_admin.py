from flask import url_for

"""
Test des controller du fichier educateur_admin.py
"""

# création d'identifiants pour les tests
login = "ALL11"
mdp = "111111"
apprenti = "ANG12"
id_fiche = 8


# test de la route de direction vers fiches apprenti
def test_route_fiches_apprenti(client):
    connexion_personnel_pin(client, login, mdp)
    response = client.get(url_for("educ_admin.fiches_apprenti", apprenti=apprenti))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/educ-admin/{apprenti}/fiches"


# test de la route de direction vers ajouter fiche
def test_route_ajouter_fiches(client):
    connexion_personnel_pin(client, login, mdp)
    response = client.get(url_for("educ_admin.ajouter_fiche", apprenti=apprenti))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == f"/educ-admin/{apprenti}/ajouter-fiche"


# test de la route de direction vers personnalisation
def test_route_personnalisation(client):
    connexion_personnel_pin(client, login, mdp)
    response = client.get(url_for("educ_admin.personnalisation", id_fiche=id_fiche))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/educ-admin/personnalisation/" + str(id_fiche)


def test_route_gestion_cours(client):
    connexion_personnel_pin(client, login, mdp)
    response = client.get(url_for("educ_admin.gestion_cours"))

    # Test d'accès à la route
    assert response.status_code == 200

    # Test de vérification de la route
    assert response.request.path == "/educ-admin/gestion-cours"
