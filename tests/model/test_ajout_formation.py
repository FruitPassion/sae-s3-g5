from unidecode import unidecode
from model_db.formation import Formation
from model_db.shared_model import db
from model.formation import add_formation

def test_ajouter_formation(client):
    intitule = "Parcours électricité"
    niveau_qualification = 3
    groupe = "1"
    image = "formation_image/elec.jpg"
    
    add_formation(intitule, niveau_qualification, groupe, image, commit=False)

    assert db.session.query(Formation).filter(Formation.intitule == intitule).first() is not None
    db.session.rollback()
    assert db.session.query(Formation).filter(Formation.intitule == intitule).first() is None