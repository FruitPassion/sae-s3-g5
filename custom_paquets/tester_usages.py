"""
Fonctions utilitaires
"""


# Fonction de connexion
def connexion_personnel(client, username, password):
    return client.post("/connexion-personnel", data=dict(
        login=username,
        password=password
    ), follow_redirects=True)


# Fonction de deconnexion
def deconnexion_personnel(client):
    return client.get('/logout', follow_redirects=True)