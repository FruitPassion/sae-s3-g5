from model_db.apprenti import Apprenti
from model_db.personnel import Personnel
from model_db.shared_model import db
from model.personnel import add_personnel
from model.apprenti import add_apprenti
from custom_paquets.converter import generate_login
from custom_paquets.security import encrypt_password

# Test de l'ajout d'un personnel
def test_ajouter_personnel(client):
    role="Educateur"
    nom="Supreme"
    prenom="Leader"
    email="mail@mail.com"
    password=encrypt_password("000000")
    login=generate_login(nom, prenom)
    
    add_personnel(login, nom, prenom, email, password, role, commit=False)
    
    assert db.session.query(Personnel).filter(Personnel.login == "LES13").first() is not None
    db.session.rollback()
    assert db.session.query(Personnel).filter(Personnel.login == "LES13").first() is None
    
#Test de l'ajout d'un apprenti
def test_ajouter_apprenti(client):
    nom="SousFifre"
    prenom="Malheureux"
    photo="/url/photo.jpg"
    login=generate_login(nom, prenom)
    
    add_apprenti(nom, prenom, login, photo, commit=False)
    
    assert db.session.query(Apprenti).filter(Apprenti.login == "MAS19").first() is not None
    db.session.rollback()
    assert db.session.query(Apprenti).filter(Apprenti.login == "MAS19").first() is None
