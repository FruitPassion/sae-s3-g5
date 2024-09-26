from flask import url_for

"""
Test des controller du fichier admin.py
"""


# Test de la route de redirection de connexion
def test_redirection_connexion(client, gestion_connexion, personnel_super_admin, check_route_status):
    # Connexion en tant que super admin
    gestion_connexion.connexion_personnel_mdp(client, personnel_super_admin)

    # Connexion à la route de connexion
    response = client.get(url_for("admin.accueil_admin"))

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/admin/accueil-admin")

    # Deconnexion de l'utilisateur
    gestion_connexion.deconnexion(client)

    # Connexion à la route de connexion
    response = client.get(url_for("admin.accueil_admin"))

    # Test du code de statut
    check_route_status.check_status(response, 302)


# Test de la route de redirection de la gestion des formations
def test_redirection_gestion_formations(client, gestion_connexion, personnel_super_admin, check_route_status):
    # Connexion en tant que super admin
    gestion_connexion.connexion_personnel_mdp(client, personnel_super_admin)

    # Connexion à la route de gestion des formations
    response = client.get(url_for("admin.gestion_formations"))

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/admin/gestion-formations")

    # Deconnexion de l'utilisateur
    gestion_connexion.deconnexion(client)

    # Connexion à la route de connexion
    response = client.get(url_for("admin.gestion_formations"))

    # Test du code de statut
    check_route_status.check_status(response, 302)


# Test de la route de redirection de la gestion des apprentis
def test_redirection_gestion_apprentis(client, gestion_connexion, personnel_super_admin, check_route_status):
    # Connexion en tant que super admin
    gestion_connexion.connexion_personnel_mdp(client, personnel_super_admin)

    # Connexion à la route de gestion des apprentis
    response = client.get(url_for("admin.gestion_apprentis"))

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/admin/gestion-apprentis")

    # Deconnexion de l'utilisateur
    gestion_connexion.deconnexion(client)

    # Connexion à la route de connexion
    response = client.get(url_for("admin.gestion_apprentis"))

    # Test du code de statut
    check_route_status.check_status(response, 302)


# Test de la route de redirection de la gestion du personnel
def test_redirection_gestion_personnel(client, gestion_connexion, personnel_super_admin, check_route_status):
    # Connexion en tant que super admin
    gestion_connexion.connexion_personnel_mdp(client, personnel_super_admin)

    # Connexion à la route de gestion du personnel
    response = client.get(url_for("admin.gestion_personnel"))

    # Test d'accès à la route et au code de statut
    check_route_status.check_both(response, 200, "/admin/gestion-personnel")

    # Deconnexion de l'utilisateur
    gestion_connexion.deconnexion(client)

    # Connexion à la route de connexion
    response = client.get(url_for("admin.gestion_personnel"))

    # Test du code de statut
    check_route_status.check_status(response, 302)
