from custom_paquets.converter import convert_to_dict
from model.formation import get_formation_id

from model_db.shared_model import db
from model_db.apprenti import Apprenti
from model_db.assister import Assister
from model_db.formation import Formation


def get_apprentis_by_formation(nom_formation: str):
    """
    Retourn la liste de tout les apprentis inscris à une formation

    :return: Une liste d'apprentis
    """
    return convert_to_dict(Assister.query.filter_by(id_formation=get_formation_id(nom_formation)).join(
        Apprenti).with_entities(Apprenti.nom, Apprenti.prenom, Apprenti.login, Apprenti.photo).
                           all())
