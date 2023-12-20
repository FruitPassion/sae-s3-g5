from model.personnel import get_id_personnel_by_login, add_personnel, archiver_personnel
from model.apprenti import add_apprenti, archiver_apprenti
from model.shared_model import db, Apprenti, Personnel
from custom_paquets.converter import generate_login
from custom_paquets.security import encrypt_password

# Création d'un personnel à ajouter puis archiver
role="Educateur"
nom_personnel="Supreme"
prenom_personnel="Leader"
email="mail@mail.com"
pwd_personnel=encrypt_password("000000")
login_personnel=generate_login(nom_personnel, prenom_personnel)
personnel = Personnel(login=login_personnel, nom=nom_personnel, prenom=prenom_personnel, email=email, mdp=pwd_personnel, role=role)

# Création d'un apprenti à ajouter puis archiver
nom_apprenti="SousFifre"
prenom_apprenti="Malheureux"
photo="/url/photo.jpg"
login_apprenti=generate_login(nom_apprenti, prenom_apprenti)
apprenti = Apprenti(nom=nom_apprenti, prenom=prenom_apprenti, login=login_apprenti, photo=photo)

# Test d'archivage d'un apprenti
def test_archiver_apprenti(client):
    id_apprenti = add_apprenti(login_apprenti, nom_apprenti, prenom_apprenti, photo, commit=False)
    archiver_apprenti(id_apprenti, archiver=True, commit=False)
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti, Apprenti.archive == 1).first() != None
    db.session.rollback()
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti, Apprenti.archive == 1).first() == None
    
# Test d'archivage d'un personnel
def test_archiver_personnel(client):
    add_personnel(login_personnel, nom_personnel, prenom_personnel, email, pwd_personnel, role, commit=False)
    id_personnel = get_id_personnel_by_login(login_personnel)
    archiver_personnel(id_personnel, archiver=True, commit=False)
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel, Personnel.archive == 1).first() != None
    db.session.rollback()
    assert db.session.query(Personnel).filter(Personnel.id_personnel == id_personnel, Personnel.archive == 1).first() == None