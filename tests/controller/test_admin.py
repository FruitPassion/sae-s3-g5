from flask import url_for
import unidecode
from custom_paquets.custom_form import AjouterPersonnel
from model_db.personnel import Personnel
from model_db.shared_model import db
from custom_paquets.tester_usages import connexion_personnel

'''
Test des controller du fichier admin.py
'''


# Test de la route de redirection de connexion
def test_redirection_connexion(client):
    # Test connexion superadministrateur
    username = "JED10"
    passw = "superadmin"
    connexion_personnel(client, username, passw)

    response = client.get(url_for("admin.accueil_admin"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/accueil-admin"


# Test de la route de redirection de la gestion des formations
def test_redirection_gestion_formation(client):
    response = client.get(url_for("admin.gestion_formation"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/gestion-formation"


# Test de la route de redirection de la gestion des apprentis
def test_redirection_gestion_apprentis(client):
    response = client.get(url_for("admin.gestion_apprenti"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/gestion-apprenti"


# Test de la route de redirection de la gestion du personnel
def test_redirection_gestion_personnel(client):
    response = client.get(url_for("admin.gestion_personnel"))

    # Test d'accès à la route
    assert response.status_code == 302

    # Test de vérification de la route
    assert response.request.path == "/admin/gestion-personnel" 

"""
JSP COMMENT FAIRE HELP
# Test de l'ajout d'un personnel
def test_ajouter_personnel(client):
    try:
        form = AjouterPersonnel()
        data = dict(
            role="Educateur",
            nom="Supreme",
            prenom="Leader",
            email="mail@mail.com",
            password="000000",
            login=unidecode(form.nom.data[0:2].upper().strip()) + unidecode(form.prenom.data[0].upper().strip()) + str(
                len(form.nom.data.strip() + form.prenom.data.strip())).zfill(2)
        )
        response = client.post(url_for("admin.gestion_personnel"), data=data)
    finally:
        response = client.get(url_for("admin.gestion_personnel"))
        assert response.status_code == 302
        assert response.request.path == "/admin/gestion-personnel"
        assert db.session.query(Personnel).filter(Personnel.login == "LES13").first() is not None
        db.rollback()
"""
"""
A VERIFIER AUSSI

def test_ajouter_formation(client):
    try:
        form = AjouterFormation()
        data = {
            "intitule": "Parcours élèctricité",
            "niveau_qualif": "3",
            "groupe": "1",
            "image": "formation_image/electricite.jpg",
            "archive" :"0"
        }

        response = client.post(url_for("admin.gestion_formations"), data=data)
        assert response.status_code == 302 

        formation_ajoutee = db.session.query(Formation).filter(Formation.intitule == data["intitule"]).first()
        assert formation_ajoutee is not None

    finally:
        response = client.get(url_for("admin.gestion_formation"))
        assert response.status_code == 302 

        db.session.rollback()
"""