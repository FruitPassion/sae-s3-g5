from model_db.formation import Formation
from model_db.shared_model import db

def test_archiver_formation(client):
    
    id_formation = 2
    
    # Récupérer la formation existante
    formation = Formation.query.filter_by(id_formation=id_formation).first()
   
    # Vérifier que la formation existe
    if not formation:
        raise ValueError(f"Aucune formation trouvée avec l'id {id_formation}")

    # Archiver la formation
    formation.archive = True

    # N'oubliez pas de rouler (commit) les modifications dans la base de données 
    db.session.commit()

    # Vérifier que la formation a bien été archivée de la base de données
    assert db.session.query(Formation).get(id_formation).archive == True

    # Effectuer d'autres vérifications si nécessaire   
    db.session.rollback()