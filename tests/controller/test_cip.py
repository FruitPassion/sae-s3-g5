from flask import url_for

'''
Test des controller du fichier cip.py
'''


# Test de la route de redirection de connexion de la CIP
def test_redirection_connexion(client, gestion_connexion, personnel_cip, check_route_status):
    gestion_connexion.connexion_personnel_pin(client, personnel_cip)
    
    response = client.get(url_for("personnel.choix_formation"))
    
    
    check_route_status.check_both(response, 200, "/personnel/choix-formation-personnel")


# Test de la route choix formation (affichage liste apprentis de cette formation)
def test_affichage_apprentis_formation(client, gestion_connexion, personnel_cip, check_route_status, formation):
    gestion_connexion.connexion_personnel_pin(client, personnel_cip)
    
    response = client.get(url_for("personnel.choix_eleve", nom_formation=formation.intitule))
    
    check_route_status.check_both(response, 200, f"/personnel/choix-eleves/{formation.intitule}")

"""
# Test de la route choix apprenti (affichage des opérations possibles pour la CIP)
def test_choix_apprenti(client, gestion_connexion, personnel_cip, check_route_status, apprenti_formation, formation):
    gestion_connexion.connexion_personnel_pin(client, personnel_cip)
    
    response = client.get(url_for("cip.affiche_choix", apprenti=apprenti_formation.login))
    print(response.request.path)
    check_route_status.check_both(response, 200, f"/cip/{apprenti_formation.login}/choix-operations")"""


# Test de la route choix fiche apprenti (affichage des fiches techniques de DAJ12)
def test_choix_fiche(client, gestion_connexion, personnel_cip, check_route_status, apprenti_formation):
    gestion_connexion.connexion_personnel_pin(client, personnel_cip)
    
    response = client.get(url_for("cip.fiches_apprenti", apprenti=apprenti_formation.login))
    
    check_route_status.check_both(response, 200, f"/cip/{apprenti_formation.login}/fiches")


# Test de la route suivi de progression de l'apprenti
def test_suivi_progression(client, gestion_connexion, personnel_cip, check_route_status, apprenti_formation):
    gestion_connexion.connexion_personnel_pin(client, personnel_cip)
    
    response = client.get(url_for("cip.suivi_progression_apprenti", apprenti=apprenti_formation.login))
    
    check_route_status.check_both(response, 200, f"/cip/{apprenti_formation.login}/suivi-progression")


# Test de la route de l'adaptation en situation d'examen de l'apprenti 
def test_adaptation_situation_exam(client, gestion_connexion, personnel_cip, apprenti_formation, check_route_status):
    gestion_connexion.connexion_personnel_pin(client, personnel_cip)
    
    response = client.get(url_for("cip.affichage_adaptation_situation_examen", apprenti = apprenti_formation.login))
    
    check_route_status.check_both(response, 200, f"/cip/{apprenti_formation.login}/adaptation-situation-examen")

