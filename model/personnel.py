from custom_paquets.converter import convertToDict

from model_db.shared_model import db
from model_db.personnel import Personnel


def getAllPersonnel():
    """
    Récupère l'id, nom, prenom et role de chaque membre du personnel

    :return: La liste des membres du personnel
    """
    personnel = Personnel.query.with_entities(Personnel.Id_Personnel, Personnel.Nom, Personnel.Prenom,
                                              Personnel.Role).all()
    return convertToDict(personnel)
