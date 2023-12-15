from unidecode import unidecode
from model_db.apprenti import Apprenti
from model_db.personnel import Personnel
from model_db.shared_model import db

# Test de l'ajout d'un personnel
def test_ajouter_personnel(client):
    role="Educateur"
    nom="Supreme"
    prenom="Leader"
    email="mail@mail.com"
    password="000000".__hash__()
    login=unidecode(prenom[0:2].upper().strip()) + unidecode(nom[0].upper().strip()) + str(
            len(nom.strip() + prenom.strip())).zfill(2)
    
    ## Copie du code dans add_personnel pour tester la fonction et éviter les commit() dans les tests
    personnel = Personnel(login = login, nom = nom, prenom = prenom, email = email, mdp = password, role = role)
    db.session.add(personnel)
    
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
    
    ## Copie du code dans add_apprenti pour tester la fonction et éviter les commit() dans les tests
    apprenti = Apprenti(nom=nom, prenom=prenom, login=login, photo=photo)
    db.session.add(apprenti)
    
    assert db.session.query(Apprenti).filter(Apprenti.login == "MAS19").first() is not None
    db.session.rollback()
    assert db.session.query(Apprenti).filter(Apprenti.login == "MAS19").first() is None