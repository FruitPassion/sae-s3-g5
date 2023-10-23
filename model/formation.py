from custom_paquets.converter import convertToDict

from model_db.shared_model import db
from model_db.formation import Formation


def getAllFormation():
    """
    Retourn la liste de toute les formations

    :return: Une liste des formations
    """
    return convertToDict(Formation.query.with_entities(Formation.id_formation, Formation.intitule).all())


def getFormationId(nom_formation: str):
    """
    Retourn l'id d'une formation a partir de son nom

    :return: Un id de formation
    """
    return Formation.query.with_entities(Formation.id_formation).filter_by(intitule=nom_formation).first().id_formation
