from flask import url_for
from model_db.formation import Formation
from model_db.shared_model import db

def test_archiver_formation(client):
    # Récupérez l'ID de la formation existante
    id_formation = formation.id

    # Récupérer la formation existante
    formation = Formation.query.filter_by(id_formation=id_formation).first()


    if not formation:
        raise ValueError(f"Aucune formation trouvée avec l'id {id_formation}")

    # Envoi de la requête POST pour archiver la formation
    formation.archive = True

    # N'oubliez pas de rouler (commit) les modifications dans la base de données 
    db.session.commit()

    # Vérifier que la formation a bien été archivée de la base de données
    assert db.session.query(Formation).get(id_formation) is None

    # Effectuer d'autres vérifications si nécessaire   
    db.session.rollback()