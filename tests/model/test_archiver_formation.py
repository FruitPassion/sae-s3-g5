from model_db.shared_model import db, Formation
from model.formation import archiver_formation, add_formation, get_formation_id

# Création d'une formation à archiver
intitule = "Parcours électricité"
niveau_qualification = 3
groupe = "1"
image = "formation_image/elec.jpg"
archive = 0

def test_archiver_formation(client):
    
    add_formation(intitule, niveau_qualification, groupe, image, commit=False)
    id_formation = get_formation_id(intitule)
    archiver_formation(id_formation, archiver=True, commit=False)
    assert db.session.query(Formation).filter(Formation.id_formation == id_formation, Formation.archive == 1).first() != None  
    db.session.rollback()
    assert db.session.query(Formation).filter(Formation.id_formation == id_formation, Formation.archive == 1).first() == None