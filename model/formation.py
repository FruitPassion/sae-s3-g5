from custom_paquets.converter import convert_to_dict

from model_db.shared_model import db
from model_db.formation import Formation


def get_all_formation():
    """
    Retourne la liste de toutes les formations

    :return: Une liste des formations
    """
    return convert_to_dict(Formation.query.with_entities(Formation.id_formation,
                                                         Formation.intitule, Formation.niveau_qualif, Formation.groupe, Formation.image).all())


def get_formation_id(nom_formation: str):
    """
    Retourne l'id d'une formation à partir de son nom

    :return: Un id de formation
    """
    return Formation.query.with_entities(Formation.id_formation).filter_by(intitule=nom_formation).first().id_formation



def get_nom_formation(id_formation):
    """
    Retourne l'intitulé d'une formation à partir de son id

    :return: Un intitulé de formation
    """
    return Formation.query.with_entities(Formation.intitule).filter_by(id_formation = id_formation).first().intitule



def add_formation(intitule, niveau_qualif, groupe, image) :
    """
    Ajoute une formation en BD

    :return: id_formation
    """
    formation = Formation(intitule = intitule, niveau_qualif = niveau_qualif, groupe = groupe, image = image)
    db.session.add(formation)
    db.session.commit()
    return formation.id_formation



def delete_formation(id_formation):
    """
    Supprime une formation en BD à partir de son id

    :param id_formation
    """
    formation = Formation.query.get(id_formation)
    db.session.delete(formation)
    db.session.commit()