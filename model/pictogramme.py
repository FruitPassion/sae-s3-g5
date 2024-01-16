import logging

from model.shared_model import ComposerPresentation as Compo, Pictogramme


def get_pictogrammes(id_fiche=1):
    """
    Récupère tous les pictogrammes associés à une fiche

    :return: les pictogrammes associés de la fiche id_fiche
    """
    try:
        return Pictogramme.query.join(Compo).filter(Compo.id_fiche != id_fiche).distinct().all()
    except Exception as e:
        logging.error("Erreur lors de la récupération des pictogrammes")
        logging.error(e)


def get_all_pictogrammes():
    """
    Récupère tous les pictogrammes

    :return: tous les pictogrammes
    """
    try:
        return Pictogramme.query.all()
    except Exception as e:
        logging.error("Erreur lors de la récupération des pictogrammes")
        logging.error(e)


def get_pictogramme_by_url(url):
    """
    Récupère un pictogramme par son url

    :param url: url du pictogramme
    :return: retourne un dictionnaire avec l'id du pictogramme
    """
    try:
        return Pictogramme.query.filter_by(url=url).with_entities(Pictogramme.id_pictogramme).first()
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du pictogramme d'URL {url}")
        logging.error(e)
