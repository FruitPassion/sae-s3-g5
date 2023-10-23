from custom_paquets.converter import convertToDict
from model.formation import getFormationId

from model_db.shared_model import db
from model_db.apprenti import Apprenti
from model_db.assister import Assister
from model_db.formation import Formation


def getApprentisByFormation(nom_formation: str):
    """
    Retourn la liste de tout les apprentis inscris à une formation

    :return: Une liste d'apprentis
    """
    return convertToDict(Assister.query.filter_by(id_formation=getFormationId(nom_formation)).join(
        Apprenti).with_entities(Apprenti.nom, Apprenti.prenom, Apprenti.login, Apprenti.photo).
                         all())
