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
personnel = Personnel(nom=nom_personnel, prenom=prenom_personnel, login=login_personnel, mdp=password, role=role, email=email)

# Création d'un apprenti à modifier
nom_apprenti="SousFifre"
prenom_apprenti="Malheureux"
photo="/url/photo.jpg"
login_apprenti=generate_login(nom_apprenti, prenom_apprenti)
apprenti = Apprenti(nom=nom_apprenti, prenom=prenom_apprenti, login=login_apprenti, photo=photo)

def test_modifier_personnel(client):
    add_personnel(login_personnel, nom_personnel, prenom_personnel, email, password, role, commit=False)
    id_personnel = get_id_personnel_by_login(login_personnel)
    
    new_role="Educateur Administrateur"

    update_personnel(id_personnel, login_personnel, nom_personnel, prenom_personnel, email, password, new_role, commit=False)

    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel).first() is not None
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel).first().role == new_role

    db.session.rollback()

def test_modifier_apprenti(client):
    id_apprenti=add_apprenti(login_apprenti, nom_apprenti, prenom_apprenti, photo, commit=False)

    new_photo="/url/photo2.jpg"

    update_apprenti(id_apprenti, login_apprenti, nom_apprenti, prenom_apprenti, password, new_photo, commit=False)

    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti).first() is not None
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti).first().photo == new_photo

    db.session.rollback()
    
