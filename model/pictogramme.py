import logging
from custom_paquets.gestions_erreur import suplement_erreur

from model.shared_model import ComposerPresentation as Compo, Pictogramme, db


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


def remove_picto(id_pictogramme, commit=True):
    """
    Supprime un pictogramme en BD

    :param id_pictgramme: id du pictogramme à supprimer
    :return: None
    """
    try:
        db.session.delete(Pictogramme.query.filter_by(id_pictogramme=id_pictogramme).first())
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        suplement_erreur(e, message=f"Erreur lors de la suppression du pictogramme {id_pictogramme}.")
        return False


def update_picto(identifiant, label, categorie, url, souscategorie, commit=True):
    """
    Modifie un matériel en BD

    """
    try:
        pictogramme = Pictogramme.query.filter_by(id_pictogramme = identifiant).first()
        pictogramme.label = label
        pictogramme.categorie = categorie
        pictogramme.souscategorie = souscategorie
        pictogramme.url = url
        if commit:
            db.session.commit()

    except Exception as e:
        suplement_erreur(e, message=f"Erreur lors de la modification du pictogramme {label}")


def get_photo_picto_by_id(id_pictogramme):
    try:
        return Pictogramme.query.filter_by(id_pictogramme=id_pictogramme).with_entities(id_pictogramme.url).first().url
    except Exception as e:
        suplement_erreur(e, message=f"Erreur lors de la récupération du lien de la photo du matériel {id_pictogramme}.")


def add_picto(label, categorie, souscategorie, url, commit=True):
    """
    Ajoute un pictogramme en BD

    """
    try:
        pictogramme = Pictogramme(label=label, categorie = categorie, url=url, souscategorie=souscategorie)
        db.session.add(pictogramme)
        if commit:
            db.session.commit()

    except Exception as e:
        suplement_erreur(e, message=f"Erreur lors de l'ajout du pictogramme {label} dans la catégorie {categorie}")
