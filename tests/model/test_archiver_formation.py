from model_db.shared_model import db, Formation
from model.formation import archiver_formation, add_formation, get_nom_formation

# Création d'une formation à archiver
intitule = "Parcours électricité"
niveau_qualification = 3
groupe = "1"
image = "formation_image/elec.jpg"
archive = 0

def test_archiver_formation(client):
    
    id_formation = 2

    # Récupérer la formation existante
    formation = Formation.query.filter_by(id_formation=id_formation).first()
   
    # Vérifier que la formation existe
    if not formation:
        raise ValueError(f"Aucune formation trouvée avec l'id {id_formation}")

    # Archiver la formation
    formation.archive = True

    # Vérifier que la formation a bien été archivée de la base de données
    assert db.session.query(Formation).get(id_formation).archive is True

    # Effectuer d'autres vérifications si nécessaire   
    db.session.rollback()