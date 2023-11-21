from custom_paquets.converter import convert_to_dict

from model_db.shared_model import db
from model_db.formation import Formation
from model_db.session import Session


def get_all_formation():
    """
    Retourn la liste de toute les formations

    :return: Une liste des formations
    """
    return convert_to_dict(Formation.query.with_entities(Formation.id_formation, Formation.intitule, Formation.image
                                                         ).all())


def get_formation_id(nom_formation: str):
    """
    Retourn l'id d'une formation a partir de son nom

    :return: Un id de formation
    """
    return Formation.query.with_entities(Formation.id_formation).filter_by(intitule=nom_formation).first().id_formation
