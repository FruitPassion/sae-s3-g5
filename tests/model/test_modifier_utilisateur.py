from model.shared_model import db, Personnel, Apprenti
from custom_paquets.converter import generate_login
from custom_paquets.security import encrypt_password
from model.personnel import add_personnel, update_personnel, get_id_personnel_by_login
from model.apprenti import add_apprenti, update_apprenti

# Création d'un personnel à modifier
nom_personnel = "Dupres"
prenom_personnel = "Jeanne"
login_personnel = generate_login(nom_personnel, prenom_personnel)
password=encrypt_password("121212")
role="Educateur"
email="mail@mail.com"

# Création d'un apprenti à modifier
nom_apprenti="SousFifre"
prenom_apprenti="Malheureux"
photo="/url/photo.jpg"
login_apprenti=generate_login(nom_apprenti, prenom_apprenti)

def test_modifier_personnel(client):
    add_personnel(login_personnel, nom_personnel, prenom_personnel, email, password, role, commit=False)
    id_personnel = get_id_personnel_by_login(login_personnel)
    
    # Modification de tous les champs du personnel
    new_role="Educateur Administrateur"
    new_nom="Dark"
    new_prenom="Vador"
    new_login=generate_login(new_nom, new_prenom)
    new_email="dark@mail.com"
    new_password=encrypt_password("090909")
    
    # Modification du personnel
    update_personnel(id_personnel, new_login, new_nom, new_prenom, new_email, new_password, new_role, commit=False)
    
    # Vérification que le personnel a bien été modifié
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel).first() is not None
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel).first().role == new_role
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel).first().nom == new_nom
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel).first().prenom == new_prenom
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel).first().login == new_login
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel).first().email == new_email
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel).first().mdp == new_password
    
    db.session.rollback()

def test_modifier_apprenti(client):
    id_apprenti=add_apprenti(login_apprenti, nom_apprenti, prenom_apprenti, photo, commit=False)
    
    # Modification des chmaps de l'apprenti
    new_nom = "Du Maître"
    new_prenom = "Toutou"
    new_login = generate_login(new_nom, new_prenom)
    new_photo="/url/photo2.jpg"
    
    # Modification de l'apprenti
    update_apprenti(id_apprenti, new_login, new_nom, new_prenom, password, new_photo, commit=False)
    
    # Vérification que l'apprenti soit bien modifé
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti).first() is not None
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti).first().nom == new_nom
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti).first().prenom == new_prenom
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti).first().login == new_login
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti).first().photo == new_photo

    db.session.rollback()