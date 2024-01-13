import logging
from custom_paquets.converter import convert_to_dict

from model.shared_model import ComposerPresentation as Compo, Pictogramme as Pict


def get_pictogrammes(id_fiche=1):
    """
    Récupère tous les pictogrammes associés à une fiche

    :return: les pictogrammes associés de la fiche id_fiche
    """
    try:
        return convert_to_dict(Pict.query.with_entities(Pict.id_pictogramme, Pict.url).join(Compo).filter(
            Compo.id_fiche != id_fiche).distinct().all())
    except Exception as e:
        logging.error("Erreur lors de la récupération des pictogrammes")
        logging.error(e)


def get_all_pictogrammes():
    """
    Récupère tous les pictogrammes

    :return: tous les pictogrammes
    """
    try:
        return convert_to_dict(Pict.query.with_entities(Pict.id_pictogramme, Pict.url, Pict.label, Pict.categorie,
                                                    Pict.souscategorie).all())
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
        return convert_to_dict(Pict.query.filter_by(url=url).with_entities(Pict.id_pictogramme).first())
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du pictogramme d'URL {url}")
        logging.error(e)
