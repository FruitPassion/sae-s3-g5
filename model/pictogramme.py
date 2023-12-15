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
    return convert_to_dict(pict.query.with_entities(pict.id_pictogramme, pict.url, pict.label, pict.categorie,
                           pict.souscategorie).all())
