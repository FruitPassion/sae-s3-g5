from flask import url_for

from model.cours import Cours
from model.formation import Formation

'''
Test des controller du fichier auth.py
'''

COMPTE_INC_OU_INV = b'Compte inconnu ou mot de passe invalide'

# Tests de la route d'accueil du site
def test_choix_connexion(client, check_route_status):
    response = client.get(url_for("auth.choix_connexion"))
    
    check_route_status.check_both(response, 200, "/")


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


def test_connexion_deconnexion_personnel(client, gestion_connexion, personnel_super_admin, personnel_educateur_admin, personnel_educateur, personnel_cip, check_route_status):

    # Test connexion personnel super admin
    response = gestion_connexion.connexion_personnel_mdp(client, personnel_super_admin)
    
    with client.session_transaction() as sess:
        assert sess['name'] == personnel_super_admin.login
        assert sess['role'] == personnel_super_admin.role
    
    check_route_status.check_both(response, 200, "/admin/accueil-admin")

    # Test deconnexion
    response = gestion_connexion.deconnexion(client)
    with client.session_transaction() as sess:
        assert sess.get('name') is None
        
    check_route_status.check_both(response, 200, "/")

    # Test connexion personnel educateur admin
    response = gestion_connexion.connexion_personnel_pin(client, personnel_educateur_admin)
    
    with client.session_transaction() as sess:
        assert sess['name'] == personnel_educateur_admin.login
        assert sess['role'] == personnel_educateur_admin.role

    check_route_status.check_both(response, 200, "/educ-admin/accueil-educadmin")
    
    gestion_connexion.deconnexion(client)

    # Test connexion personnel educateur
    response = gestion_connexion.connexion_personnel_pin(client, personnel_educateur)
    
    with client.session_transaction() as sess:
        assert sess['name'] == personnel_educateur.login
        assert sess['role'] == personnel_educateur.role

    check_route_status.check_both(response, 200, "/personnel/choix-formation-personnel")
    
    gestion_connexion.deconnexion(client)

    # Test connexion personnel cip
    response = gestion_connexion.connexion_personnel_pin(client, personnel_cip)
    
    with client.session_transaction() as sess:
        assert sess['name'] == personnel_cip.login
        assert sess['role'] == personnel_cip.role

    check_route_status.check_both(response, 200, "/personnel/choix-formation-personnel")
    
    gestion_connexion.deconnexion(client)




def test_connexion_deconnexion_raté(client, gestion_connexion, faux_personnel, check_route_status):
    # Test connexion personnel avec un faux personnel
    response = gestion_connexion.connexion_personnel_pin(client, faux_personnel, reset=False)
    
    assert COMPTE_INC_OU_INV in response.data
        
    check_route_status.check_both(response, 403, "/connexion-personnel-pin")
    


# Test de la route affichant la liste des formations
def test_choix_formation_apprentis(client, check_route_status, formation):
    response = client.get(url_for("auth.choix_formation_apprentis"))
        
    check_route_status.check_both(response, 200, "/choix-formation-apprentis")

    # Test de verification de l'utilisation de tout les intitules de formation
    formations = Formation.get_all_formations()
    
    html = response.get_data(as_text=True)
    for tformation in formations:
        assert tformation.intitule in html


# Test de la route affichant la liste des apprentis en fonction d'une formation
def test_choix_eleve_apprentis(client, formation, check_route_status, apprenti_formation):
    
    response = client.get(url_for("auth.choix_eleve_apprentis", nom_formation=formation.intitule))
        
    check_route_status.check_both(response, 200, f"/choix-eleve-apprentis/{formation.intitule}")

    # Test de verification de l'utilisation de toutes les informations de l'apprentis
    apprentis = Cours.get_apprentis_by_formation(formation.intitule)
    html = response.get_data(as_text=True)
    for apprenti in apprentis:
        assert 'class="libelle">' + apprenti.prenom + ' ' + apprenti.nom in html


def test_connexion_deconnexion_apprenti(client, formation, apprenti_formation, check_route_status, gestion_connexion):
    # Test accès apprenti sans login
    response = client.get(url_for("apprenti.redirection_connexion"))

    check_route_status.check_status(response, 302)
    
    # Test de connexion bon mot de passe et bon login
    response = gestion_connexion.connexion_apprentis(client, formation, apprenti_formation)

    check_route_status.check_both(response, 200, "/apprenti/redirection-connexion")
    
    with client.session_transaction() as sess:
        assert sess['name'] == apprenti_formation.login
        assert sess['role'] == 'apprentis'
    
    # Test deconnexion
    response = gestion_connexion.deconnexion(client)
    
    with client.session_transaction() as sess:
        assert sess.get('name') is None
    assert response.status_code == 200
    assert response.request.path == "/"