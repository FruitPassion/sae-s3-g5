from unidecode import unidecode
from model_db.formation import Formation
from model_db.shared_model import db

def test_ajouter_formation(client):
    intitule = "Parcours électricité"
    niveau_qualification = 3
    groupe = "1"
    image = "formation_image/elec.jpg"
    archive = 1

    formation = Formation(
        intitule=intitule,
        niveau_qualif=niveau_qualification,
        groupe=groupe,
        image=image,
        archive=archive
    )

    db.session.add(formation)

    assert db.session.query(Formation).filter(Formation.intitule == intitule).first() is not None
    db.session.rollback()
    assert db.session.query(Formation).filter(Formation.intitule == intitule).first() is None