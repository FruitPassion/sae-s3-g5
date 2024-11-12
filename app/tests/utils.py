import datetime

import json

import os
import sys
from datetime import date

from faker import Faker
from flask import url_for
from playwright.sync_api import Page, expect

from model.formation import Formation

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from custom_paquets.converter import generate_login
from model.apprenti import Apprenti
from model.cours import Cours
from model.ficheintervention import FicheIntervention
from model.personnel import Personnel

fake = Faker(["fr_FR"])


#####################################################
# Fixture pour la gestion du super administrateur   #
#####################################################


def d_super_admin():
    class PersonnelSuperAdminTest:
        def __init__(self):
            self.role = "SuperAdministrateur"
            self.nom = fake.last_name()
            self.prenom = fake.first_name()
            self.email = f"{self.prenom}.{self.nom}@{fake.domain_name()}"
            self.login = generate_login(self.nom, self.prenom)
            self.password = "superadmin"
            self.hash = "$2b$13$ZV3TQXG81BSnNEDFdSmSp.HnkMVeDlHSRXpT3wc73.OEoQ2v.4ONS"

            self.id_personnel = Personnel.add_personnel(self.login, self.nom, self.prenom, self.email, self.hash, self.role)

    return PersonnelSuperAdminTest()


#########################################################
# Fixture pour la gestion de l'éducateur administrateur #
#########################################################


def d_educ_admin():
    class PersonnelAdminTest:
        def __init__(self):
            self.role = "Educateur Administrateur"
            self.nom = fake.last_name()
            self.prenom = fake.first_name()
            self.email = f"{self.prenom}.{self.nom}@{fake.domain_name()}"
            self.login = generate_login(self.nom, self.prenom)
            self.password = "111111"
            self.hash = "$2b$13$iZbA5.LcL1xk3mJPrHAkleUUA3mpJL4qVVx6QAtY/27rQcgfykqIK"

            self.id_personnel = Personnel.add_personnel(self.login, self.nom, self.prenom, self.email, self.hash, self.role)

    return PersonnelAdminTest()


#####################################################
# Fixture pour la gestio du personnel CIP           #
#####################################################


def d_cip():
    class PersonnelCIPTest:
        def __init__(self):
            self.role = "CIP"
            self.nom = fake.last_name()
            self.prenom = fake.first_name()
            self.email = f"{self.prenom}.{self.nom}@{fake.domain_name()}"
            self.login = generate_login(self.nom, self.prenom)
            self.password = "111111"
            self.hash = "$2b$13$iZbA5.LcL1xk3mJPrHAkleUUA3mpJL4qVVx6QAtY/27rQcgfykqIK"

            self.id_personnel = Personnel.add_personnel(self.login, self.nom, self.prenom, self.email, self.hash, self.role)

    return PersonnelCIPTest()


#####################################################
# Fixture pour la gestion de l'éducateur simple     #
#####################################################


def d_educ():
    class PersonnelEducateurTest:
        def __init__(self):
            self.role = "Educateur"
            self.nom = fake.last_name()
            self.prenom = fake.first_name()
            self.email = f"{self.prenom}.{self.nom}@{fake.domain_name()}"
            self.login = generate_login(self.nom, self.prenom)
            self.password = "111111"
            self.hash = "$2b$13$iZbA5.LcL1xk3mJPrHAkleUUA3mpJL4qVVx6QAtY/27rQcgfykqIK"

            self.id_personnel = Personnel.add_personnel(self.login, self.nom, self.prenom, self.email, self.hash, self.role)

    return PersonnelEducateurTest()


#####################################################
# Fixture pour la gestion de l'apprenti             #
#####################################################


def d_apprenti():
    """
    Retourne un apprenti avec un mot de passe
    """
    formation = d_formation()

    class ApprentiTest:
        def __init__(self):
            self.nom = fake.last_name()
            self.prenom = fake.first_name()
            self.photo = "/url/photo2.jpg"
            self.login = generate_login(self.nom, self.prenom)
            self.password = "12369"
            self.archive = True

            self.id_apprenti = Apprenti.add_apprenti(self.nom, self.prenom, self.login, self.photo)
            Apprenti.set_password_apprenti(self.login, self.password)
            Cours.add_apprenti_assister(self.id_apprenti, formation.id_formation)

    return {"d_formation": formation, "d_apprenti": ApprentiTest()}


def d_apprenti_sans_mdp():
    """
    Retourne un apprenti sans mot de passe
    """

    class ApprentiTestSansMdp:
        def __init__(self):
            self.nom = fake.last_name()
            self.prenom = fake.first_name()
            self.photo = "/url/photo2.jpg"
            self.login = generate_login(self.nom, self.prenom)
            self.archive = True
            self.password = "111111"

            self.id_apprenti = Apprenti.add_apprenti(self.nom, self.prenom, self.login, self.photo)

    return ApprentiTestSansMdp()


#####################################################
# Fixture pour la création de fiche                 #
#####################################################


def d_fiche():
    cour = d_cour()
    apprenti = d_apprenti()
    educ_admin = d_educ_admin()

    class FicheTest:
        def __init__(self):
            self.nom_du_demandeur = fake.first_name()
            self.date_demande = datetime.date.today()
            self.localisation = fake.city()
            self.description_demande = fake.text()
            self.degre_urgence = fake.random_int(min=1, max=4)
            self.couleur_intervention = ["rouge", "orange", "jaune", "vert"][self.degre_urgence - 1]
            self.etat_fiche = 0
            self.date_creation = datetime.datetime.now()
            self.photo_avant = None
            self.photo_apres = None
            self.nom_intervenant = fake.last_name()
            self.prenom_intervenant = fake.first_name()
            self.id_apprenti = apprenti.id_apprenti
            self.id_personnel = educ_admin.id_personnel
            self.id_cours = cour.id_cours

            self.id_fiche = FicheIntervention.assigner_fiche_dummy_eleve(
                apprenti.login,
                self.id_personnel,
                self.date_demande,
                self.nom_du_demandeur,
                self.localisation,
                self.description_demande,
                self.degre_urgence,
                self.couleur_intervention,
                self.nom_intervenant,
                self.prenom_intervenant,
                self.id_cours,
            )
            self.numero = FicheIntervention.get_fiche_par_id_fiche(self.id_fiche).numero

    return {"d_cour": cour, "d_apprenti": apprenti, "d_educ_admin": educ_admin, "d_fiche": FicheTest()}


#####################################################
# Fixture pour la gestion des formations et cours   #
#####################################################


def d_formation():
    class FormationTest:
        def __init__(self):
            formation = Formation.get_all_formations()[0]
            self.id_formation = formation.id_formation
            self.intitule = formation.intitule
            self.niveau_qualif = formation.niveau_qualif
            self.groupe = formation.groupe
            self.image = formation.image

    return FormationTest()


def d_formation_fausse():
    class FormationTest:
        def __init__(self):
            self.intitule = "Parcours Dinguerie"

    return FormationTest()


def d_cour():
    class CoursTest:
        def __init__(self):
            cour = Cours.get_all_cours()[0]
            self.id_cours = cour.id_cours
            self.theme = cour.theme
            self.cours = cour.cours
            self.duree = cour.duree
            self.id_formation = cour.id_formation

    return CoursTest()


#####################################################
# Fixture pour la gestion du faux personnel         #
#####################################################


def d_faux_personnel():
    class FauxPersonnel:
        def __init__(self):
            self.role = "SuperAdministrateur"
            self.nom = fake.last_name()
            self.prenom = fake.first_name()
            self.email = f"{self.prenom}.{self.nom}@{fake.domain_name()}"
            self.login = generate_login(self.nom, self.prenom)
            self.password = "654321"

    return FauxPersonnel()


##########################################################################
# Fixture pour la gestion de l'import et de l'export des donnée en json  #
##########################################################################


def create_or_delete_json(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump({}, f)
    else:
        os.remove(filename)


def extract_from_classes(classes, filename):
    instances = {}

    for class_name in classes:
        class_instance = eval(class_name + "()")
        if type(class_instance) is dict:
            for key, value in class_instance.items():
                instances[key] = value
        else:
            instances[class_name] = class_instance

    with open(filename, "w") as file:
        json.dump({class_name: instance.__dict__ for class_name, instance in instances.items()}, file, indent=4, sort_keys=True, default=str)


def restitue_classes(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    return data


def connexion_personnel_pin(page: Page, personnel: dict) -> Page:
    page.goto(url_for("auth.connexion_personnel_pin", _external=True))
    pin = [int(i) for i in personnel["password"]]
    for i in pin:
        page.locator(f"css=button:has-text('{i}')").click()
    page.get_by_role("button", name="Valider").click()


def connexion_personnel_mdp(page: Page, personnel: dict) -> Page:
    page.goto(url_for("auth.connexion_personnel_mdp", _external=True))
    page.locator("#login").click()
    page.locator("#login").fill(personnel["login"])
    page.locator("#password").click()
    page.locator("#password").fill(personnel["password"])
    page.get_by_role("button", name="Se connecter").click()
    return page
