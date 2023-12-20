from custom_paquets.converter import convert_to_dict

from model.shared_model import ComposerPresentation as Compo, Pictogramme as Pict


def get_pictogramme(id_fiche=1):
    """
    Recupere tous les pictogrammes associés à une fiche
    """
    return convert_to_dict(Pict.query.with_entities(Pict.id_pictogramme, Pict.url).join(Compo).filter(
        Compo.id_fiche != id_fiche).distinct().all())


def get_all_pictogrammes():
    """
    Recupere tous les pictogrammes
    :return:
    """
    return convert_to_dict(Pict.query.with_entities(Pict.id_pictogramme, Pict.url, Pict.label, Pict.categorie,
                                                    Pict.souscategorie).all())


def get_pictogramme_by_url(url):
    """
    Recupere un pictogramme par son url

    :param url: url du pictogramme
    :return: retourne un dictionnaire avec l'id du pictogramme
    """
    return convert_to_dict(Pict.query.filter_by(url=url).with_entities(Pict.id_pictogramme).first())
