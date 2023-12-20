import logging

from custom_paquets.converter import convert_to_dict
from model.apprenti import remove_apprenti, get_apprenti_by_formation

from model.shared_model import db, Formation, Session


def get_all_formation(archive=False):
    """
    Retourne la liste de toutes les formations

    :param archive: Si True, retourne uniquement les formations archivées
    :return: Une liste des formations
    """
    return convert_to_dict(
        Formation.query.with_entities(Formation.id_formation, Formation.intitule, Formation.niveau_qualif,
                                      Formation.groupe, Formation.image).filter(
            Formation.archive == archive).all())


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
    return Formation.query.with_entities(Formation.intitule).filter_by(id_formation=id_formation).first().intitule

def get_image_formation(id_formation):
    return Formation.query.filter_by(id_formation=id_formation).with_entities(Formation.image).first().image

def add_formation(intitule, niveau_qualif, groupe, image, commit=True):
    """
    Ajoute une formation en BD

    :return: id_formation
    """
    formation = Formation(intitule=intitule, niveau_qualif=niveau_qualif, groupe=groupe, image=image)
    db.session.add(formation)
    if commit:
        db.session.commit()
    return formation.id_formation

def update_formation(identifiant, intitule, niveau_qualif, groupe, image, commit=True):
    """
    Modifie une formation en BD

    :return: None
    """
    try:
        formation = Formation.query.filter_by(id_apprenti=identifiant).first()
        formation.intitule = intitule
        formation.niveau_qualif = niveau_qualif
        formation.image = image
        db.session.commit()
    except Exception as e:
        logging.error("Erreur lors de la modification de l'apprenti")
        logging.error(e)

def archiver_formation(id_formation, archiver=True, commit=True):
    """
    Archive une formation en BD

    :param id_formation: id de la formation à archiver
    :param archiver: True pour archiver, False pour désarchiver
    :return: None
    """
    try:
        formation = Formation.query.filter_by(id_formation=id_formation).first()
        formation.archive = archiver
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        logging.error("Erreur lors de l'archivage d'une formation")
        logging.error(e)
        return False


def get_sessions_par_formation(id_formation):
    """
    :return: toutes les sessions de la formation id_formation
    """
    return Session.query.filter_by(id_formation=id_formation).all()


def remove_formation(id_formation):
    """
    Supprime une formation en BD

    :param id_formation: id de la formation à supprimer
    :return: None
    """
    try:
        for apprenti in get_apprenti_by_formation(id_formation):
            remove_apprenti(apprenti.id_apprenti)
        db.session.commit()
        for session in get_sessions_par_formation(id_formation):
            print(session)
            db.session.delete(session)
        db.session.commit()
        Formation.query.filter_by(id_formation=id_formation).delete()
        db.session.commit()
        return True
    except Exception as e:
        logging.error("Erreur lors de la suppression d'une formation")
        logging.error(e)
        return False
