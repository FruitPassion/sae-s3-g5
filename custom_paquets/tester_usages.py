"""
Fonctions utilitaires
"""
from custom_paquets.converter import generate_login
from custom_paquets.security import encrypt_password
from model.apprenti import add_apprenti, update_apprenti
from model.formation import add_formation
from model.personnel import reset_nbr_essaies_connexion, add_personnel, update_personnel


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


class PersonnelTest:
    def __init__(self):
        self.role = "Educateur"
        self.nom = "Supreme"
        self.prenom = "Leader"
        self.email = "mail@mail.com"
        self.password = encrypt_password("000000")
        self.login = generate_login(self.nom, self.prenom)

        self.id_personnel = add_personnel(self.login, self.nom, self.prenom, self.email, self.password, self.role, commit=False)


class PersonnelTestModif:
    def __init__(self, id_personnel):
        self.id_personnel = id_personnel
        self.role = "Educateur Administrateur"
        self.nom = "Dark"
        self.prenom = "Vador"
        self.login = generate_login(self.nom, self.prenom)
        self.email = "dark@mail.com"
        self.password = encrypt_password("090909")

        update_personnel(self.id_personnel, self.login, self.nom, self.prenom, self.email, self.password, self.role,
                         commit=False)


class ApprentiTest:
    def __init__(self, commit=False):
        self.nom = "SousFifre"
        self.prenom = "Malheureux"
        self.photo = "/url/photo.jpg"
        self.login = generate_login(self.nom, self.prenom)

        self.id_apprenti = add_apprenti(self.nom, self.prenom, self.login, self.photo, commit=commit)


class ApprentiTestModif:
    def __init__(self, id_apprenti):
        self.id_apprenti = id_apprenti
        self.nom = "Du Maître"
        self.prenom = "Toutou"
        self.photo = "/url/photo2.jpg"
        self.login = generate_login(self.nom, self.prenom)
        self.password = encrypt_password("121212")
        self.actif = True

        update_apprenti(self.id_apprenti, self.login, self.nom, self.prenom, self.photo, self.password,self.actif, commit=False)


class FormationTest:
    def __init__(self, commit=False):
        self.intitule = "Parcours électricité"
        self.niveau_qualification = 3
        self.groupe = "1"
        self.image = "formation_image/elec.jpg"

        self.id_formation = add_formation(self.intitule, self.niveau_qualification, self.groupe, self.image, commit=commit)