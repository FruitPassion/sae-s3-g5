"""
Fonctions utilitaires
"""

# Fonction de connexion avec un code pin
def connexion_personnel_pin(client, username, password):
    return client.post("/connexion-personnel-pin", data=dict(
        login=username,
        password=password
    ), follow_redirects=True)

# Fonction de connexion avec un mot de passe
def connexion_personnel_mdp(client, username, password):
    return client.post("/connexion-personnel-mdp", data=dict(
        login=username,
        password=password
    ), follow_redirects=True)

# Fonction de deconnexion
def deconnexion_personnel(client):
    return client.get('/logout', follow_redirects=True)