import logging

from custom_paquets.converter import convert_to_dict
from model.apprenti import remove_apprenti, get_apprentis_by_formation

from model.shared_model import db, Formation, Cours


def get_all_formations(archive=False):
    """
    Retourne la liste de toutes les formations

    :param archive: Si True, retourne uniquement les formations archivées
    :return: Une liste de formations
    """
    try:
        return convert_to_dict(
            Formation.query.with_entities(Formation.id_formation, Formation.intitule, Formation.niveau_qualif,
                                        Formation.groupe, Formation.image).filter(
                Formation.archive == archive).all())
    except Exception as e:
        logging.error("Erreur lors de la récupération de la liste de toutes les formations")
        logging.error(e)


def get_formation_id(nom_formation: str):
    """
    Retourne l'id d'une formation à partir de son nom

    :return: Un id de formation
    """
    try:
        return Formation.query.with_entities(Formation.id_formation).filter_by(intitule=nom_formation).first().id_formation
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'id de la formation {nom_formation}")
        logging.error(e)
        return False


def get_nom_formation(id_formation):
    """
    Retourne l'intitulé d'une formation à partir de son id

    :return: Un intitulé de formation
    """
    try:
        return Formation.query.with_entities(Formation.intitule).filter_by(id_formation=id_formation).first().intitule
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du nom de la formation {id_formation}")
        logging.error(e)


def get_image_formation(id_formation):
    try:
        return Formation.query.filter_by(id_formation=id_formation).with_entities(Formation.image).first().image
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'image de la formation {id_formation}")
        logging.error(e)


def add_formation(intitule, niveau_qualif, groupe, image, commit=True):
    """
    Ajoute une formation en BD

    :return: id_formation
    """
    try:
        formation = Formation(intitule=intitule, niveau_qualif=niveau_qualif, groupe=groupe, image=image)
        db.session.add(formation)
        if commit:
            db.session.commit()
        return get_formation_id(intitule)
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout de la formation {intitule}")
        logging.error(e)


def update_formation(identifiant, intitule, niveau_qualif, groupe, image, commit=True):
    """
    Modifie une formation en BD

    :return: None
    """
    try:
        formation = Formation.query.filter_by(id_formation=identifiant).first()
        formation.intitule = intitule
        formation.niveau_qualif = niveau_qualif
        formation.groupe = groupe
        formation.image = image
        if commit:
            db.session.commit()
    except Exception as e:
        logging.error(f"Erreur lors de la modification de la formation {intitule}")
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
        logging.error(f"Erreur lors de l'archivage de la formation {id_formation}")
        logging.error(e)
        return False


def get_cours_par_formation(id_formation):
    """
    :return: tous les cours de la formation id_formation
    """
    try:
        return Cours.query.filter_by(id_formation=id_formation).all()
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des cours de la formation {id_formation}")
        logging.error(e)


def remove_formation(id_formation, commit=True):
    """
    Supprime une formation en BD

    :param id_formation: id de la formation à supprimer
    :return: None
    """
    try:
        for apprenti in get_apprentis_by_formation(id_formation):
            remove_apprenti(apprenti.id_apprenti)
        if commit:
            db.session.commit()
        for cours in get_cours_par_formation(id_formation):
            db.session.delete(cours)
        if commit:
            db.session.commit()
        db.session.delete(Formation.query.filter_by(id_formation=id_formation).first())
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la suppression de la formation {id_formation}")
        logging.error(e)
        return False


def reinitisaliser_formation(id_formation, commit=True):
    """
    Réinitialise une formation en retirant tous les apprentis et les cours d'une formation

    :param id_formation: id de la formation à réinitialiser
    :param commit: True pour commit, False pour ne pas commit
    :return: True si la réinitialisation s'est bien passée, False sinon
    """
    try:
        # TODO: appel de la génération des XLS pour les apprentis et les cours
        # generer_xls_apprentis(id_formation)
        # generer_xls_cours(id_formation)

        # Suppression des apprentis
        for apprenti in get_apprentis_by_formation(id_formation):
            remove_apprenti(apprenti.id_apprenti)

        if commit:
            db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la réinitisalisation de la formation {id_formation}")
        logging.error(e)
        return False
