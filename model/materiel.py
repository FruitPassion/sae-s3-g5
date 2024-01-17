from model.shared_model import Materiel


def get_all_materiel():
    """
    Récupère tout le matériel

    :return: liste de tous les matériels
    """
    return Materiel.query.all()