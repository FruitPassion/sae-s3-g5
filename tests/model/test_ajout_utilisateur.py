from unidecode import unidecode
from model_db.shared_model import db, Personnel, Apprenti
from model.personnel import add_personnel
from model.apprenti import add_apprenti

# Test de l'ajout d'un personnel
def test_ajouter_personnel(client):
    role="Educateur"
    nom="Supreme"
    prenom="Leader"
    email="mail@mail.com"
    password="000000".__hash__()
    login=unidecode(prenom[0:2].upper().strip()) + unidecode(nom[0].upper().strip()) + str(
            len(nom.strip() + prenom.strip())).zfill(2)
    
    add_personnel(login, nom, prenom, email, password, role, commit=False)
    
    assert db.session.query(Personnel).filter(Personnel.login == "LES13").first() is not None
    db.session.rollback()
    assert db.session.query(Personnel).filter(Personnel.login == "LES13").first() is None


#Test de l'ajout d'un apprenti
def test_ajouter_apprenti(client):
    nom="SousFifre"
    prenom="Malheureux"
    photo="/url/photo.jpg"
    login=unidecode(prenom[0:2].upper().strip()) + unidecode(nom[0].upper().strip()) + str(
            len(nom.strip() + prenom.strip())).zfill(2)
    
    add_apprenti(nom, prenom, login, photo, commit=False)
    
    assert db.session.query(Apprenti).filter(Apprenti.login == "MAS19").first() is not None
    db.session.rollback()
    assert db.session.query(Apprenti).filter(Apprenti.login == "MAS19").first() is None
