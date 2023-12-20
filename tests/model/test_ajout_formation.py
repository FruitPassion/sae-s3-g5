from model.shared_model import db, Formation
from model.formation import add_formation

def test_ajouter_formation(client):
    intitule = "Parcours électricité"
    niveau_qualification = 3
    groupe = "1"
    image = "null"
    
    add_formation(intitule, niveau_qualification, groupe, image, commit=False)

    assert db.session.query(Formation).filter(Formation.intitule == intitule).first() is not None
    db.session.rollback()
    assert db.session.query(Formation).filter(Formation.intitule == intitule).first() is None