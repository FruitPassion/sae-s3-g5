from custom_paquets.converter import convert_to_dict

from model_db.shared_model import db
from model_db.pictogramme import Pictogramme as pict
from model_db.ficheintervention import FicheIntervention
from model_db.elementbase import ElementBase as elem
from model_db.composer import ComposerPresentation as compo


def get_pictogramme(id_fiche=1):
    """
    Recupere tous les pictogrammes associés à une fiche
    """
    return convert_to_dict(pict.query.with_entities(pict.id_pictogramme, pict.url).join(compo).filter(
        compo.id_fiche != id_fiche).distinct().all())


def get_all_pictogrammes():
    """
    Recupere tous les pictogrammes
    :return:
    """
    return convert_to_dict(pict.query.with_entities(pict.id_pictogramme, pict.url, pict.label, pict.categorie,
                           pict.souscategorie).all())


def get_pictogramme_by_url(url):
    """
    Recupere un pictogramme par son url

    :param url: url du pictogramme
    :return: retourne un dictionnaire avec l'id du pictogramme
    """
    return convert_to_dict(pict.query.filter_by(url=url).with_entities(pict.id_pictogramme).first())
