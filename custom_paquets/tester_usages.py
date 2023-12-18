"""
Fonctions utilitaires
"""
from model.personnel import reset_nbr_essaies_connexion


# Fonction de connexion avec un code pin
def connexion_personnel_pin(client, username, password):
    reset_nbr_essaies_connexion(username)
    return client.post("/connexion-personnel-pin", data=dict(
        login_select=username,
        code=password
    ), follow_redirects=True)


# Fonction de connexion avec un mot de passe
def connexion_personnel_mdp(client, username, password):
    reset_nbr_essaies_connexion(username)
    return client.post("/connexion-personnel-mdp", data=dict(
        login=username,
        password=password
    ), follow_redirects=True)


# Fonction de deconnexion
def deconnexion_personnel(client):
    return client.get('/logout', follow_redirects=True)
