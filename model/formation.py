from custom_paquets.converter import convertToDict

from model_db.shared_model import db
from model_db.formation import Formation


def getAllFormation():
    """
    Retourn la liste de toute les formations

    :return: Une liste des formations
    """
    return convertToDict(Formation.query.with_entities(Formation.id_formation, Formation.intitule).all())
