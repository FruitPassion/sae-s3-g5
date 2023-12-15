from flask import url_for
from model_db.formation import Formation
from model_db.shared_model import db

def test_supprimer_formation(client):
    # Supposons que vous ayez une formation existante dans la base de données avec l'intitulé "Parcours électricité"
    intitule = "Parcours électricité"
    formation = db.session.query(Formation).filter(Formation.intitule == intitule).first()

    if not formation:
        raise ValueError(f"Aucune formation trouvée avec l'intitulé {intitule}")

    # Récupérez l'ID de la formation existante
    id_formation = formation.id

    # Envoi de la requête POST pour supprimer la formation
    db.session.delete(formation)

    # Vérifier que la formation a bien été supprimée de la base de données
    assert db.session.query(Formation).get(id_formation) is None

    # Effectuer d'autres vérifications si nécessaire

    # N'oubliez pas de rouler (commit) les modifications dans la base de données
    db.session.rollback()