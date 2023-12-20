from model.shared_model import FicheIntervention, db, Apprenti
from model.apprenti import add_apprenti, remove_apprenti
from custom_paquets.converter import generate_login

# Création d'un apprenti à ajouter puis supprimer
nom_apprenti="SousFifre"
prenom_apprenti="Malheureux"
photo="/url/photo.jpg"
login_apprenti=generate_login(nom_apprenti, prenom_apprenti)
apprenti = Apprenti(nom=nom_apprenti, prenom=prenom_apprenti, login=login_apprenti, photo=photo)

def test_supprimer_apprenti(client):
    id_apprenti = add_apprenti(login_apprenti, nom_apprenti, prenom_apprenti, photo, commit=False)
    
    remove_apprenti(id_apprenti, commit=False)
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti).first() == None
    assert FicheIntervention.query.filter_by(id_apprenti=id_apprenti).all() == []
    db.session.rollback()