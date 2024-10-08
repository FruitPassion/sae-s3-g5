"""
Fonctions utilitaires
"""

from custom_paquets.converter import generate_login
from custom_paquets.security import encrypt_password
from model.apprenti import Apprenti
from model.cours import Cours
from model.formation import Formation
from model.personnel import Personnel


# Fonction de connexion avec un code pin
def connexion_personnel_pin(client, username, password):
    Personnel.reset_nbr_essais_connexion(username)
    return client.post("/connexion-personnel-pin", data=dict(login_select=username, code=password), follow_redirects=True)


# Fonction de connexion avec un mot de passe
def connexion_personnel_mdp(client, username, password):
    Personnel.reset_nbr_essais_connexion(username)
    return client.post("/connexion-personnel-mdp", data=dict(login=username, password=password), follow_redirects=True)


# Fonction de connexion avec un mot de passe
def connexion_apprentis(client, nom_formation, login, password):
    Apprenti.reset_nbr_essais_connexion(login)
    return client.post(f"/connexion-apprentis/{nom_formation}/{login}", data=dict(login=login, password=password), follow_redirects=True)


# Fonction de deconnexion
def deconnexion(client):
    return client.get("/logout", follow_redirects=True)


class PersonnelTest:
    def __init__(self):
        self.role = "Educateur"
        self.nom = "Supreme"
        self.prenom = "Leader"
        self.email = "mail@mail.com"
        self.password = encrypt_password("000000")
        self.login = generate_login(self.nom, self.prenom)

        self.id_personnel = Personnel.add_personnel(self.login, self.nom, self.prenom, self.email, self.password, self.role, commit=False)


class PersonnelTestModif:
    def __init__(self, id_personnel):
        self.id_personnel = id_personnel
        self.role = "Educateur Administrateur"
        self.nom = "Dark"
        self.prenom = "Vador"
        self.login = generate_login(self.nom, self.prenom)
        self.email = "dark@mail.com"
        self.password = encrypt_password("090909")

        Personnel.update_personnel(self.id_personnel, self.login, self.nom, self.prenom, self.email, self.password, self.role, commit=False)


class ApprentiTest:
    def __init__(self):
        self.nom = "SousFifre"
        self.prenom = "Malheureux"
        self.photo = "/url/photo.jpg"
        self.login = generate_login(self.nom, self.prenom)

        self.id_apprenti = Apprenti.add_apprenti(self.nom, self.prenom, self.login, self.photo)


class ApprentiTestModif:
    def __init__(self, id_apprenti):
        self.id_apprenti = id_apprenti
        self.nom = "Du Maître"
        self.prenom = "Toutou"
        self.photo = "/url/photo2.jpg"
        self.login = generate_login(self.nom, self.prenom)
        self.password = encrypt_password("121212")
        self.actif = True

        Apprenti.update_apprenti(self.id_apprenti, self.login, self.nom, self.prenom, self.photo, self.password, self.actif)


class FormationTest:
    def __init__(self):
        self.intitule = "Parcours électricité"
        self.niveau_qualification = 3
        self.groupe = "1"
        self.image = "formation_image/elec.jpg"

        self.id_formation = Formation.add_formation(self.intitule, self.niveau_qualification, self.groupe, self.image)


class CoursTest:
    def __init__(self, commit=False):
        self.theme = "Electrique"
        self.cours = "Réparer un branchement électrique"
        self.duree = 5
        self.id_formation = 2

        self.id_cours = Cours.add_cours(self.theme, self.cours, self.duree, self.id_formation, commit=commit)


class CoursTestModif:
    def __init__(self, id_cours):
        self.id_cours = id_cours
        self.theme = "Serrurier"
        self.cours = "Réparer une serrure"
        self.duree = 2
        self.archive = False

        Cours.update_cours(self.id_cours, self.theme, self.cours, self.duree, commit=False)
