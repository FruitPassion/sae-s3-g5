from custom_paquets.converter import convert_to_dict
from model_db.ficheintervention import FicheIntervention
from model_db.elementbase import ElementBase as elem
from model_db.composer import ComposerPresentation as compo
from model_db.pictogramme import Pictogramme as pict
from model_db.shared_model import db


def get_composer_presentation(id_fiche=1):
    """
    Permet de recuperer toutes les catégories d'une fiche

    :return: liste de dictionnaires
    """
    return convert_to_dict(
        compo.query.filter_by(id_fiche=id_fiche).with_entities(compo.id_element, compo.id_pictogramme,
                                                               compo.text, compo.taille_texte,
                                                               compo.police, compo.taille_pictogramme,
                                                               compo.audio, compo.police,
                                                               compo.couleur, compo.couleur_fond,
                                                               compo.niveau,
                                                               compo.position_elem,
                                                               compo.ordre_saisie_focus).all())


def get_composer_categorie(id_fiche=1):
    """
    Permet de recuperer toutes les catégories d'une fiche

    :return: liste de dictionnaires
    """
    return convert_to_dict(compo.query.filter_by(
        id_fiche=id_fiche).with_entities(compo.id_element, compo.id_pictogramme, compo.text, compo.taille_texte,
                                         compo.police,
                                         compo.audio, compo.police, compo.couleur, compo.couleur_fond, compo.niveau,
                                         compo.position_elem, compo.ordre_saisie_focus).join(
        elem).filter_by(type="categorie").all())


def get_composer_non_categorie(id_fiche=1):
    """
    Permet tous les elements d'une fiche associés à une catégorie

    :return: liste de dictionnaires
    """
    return convert_to_dict(
        db.session.query(compo.id_element, compo.text, compo.taille_texte, compo.police, compo.audio, compo.police,
                         compo.couleur, compo.couleur_fond, compo.niveau, compo.position_elem, compo.taille_pictogramme,
                         compo.ordre_saisie_focus, compo.id_pictogramme.label("pictogramme"), compo.taille_pictogramme
                         ).filter_by(id_fiche=id_fiche).join(elem).filter(elem.type != "categorie").all())


def get_elements_base():
    """
    Permet de recuprer les elements de base de la table ComposerPresentation

    :return: liste de dictionnaires avec l'id, le libelle, le type et l'url audio des elements
    """
    return convert_to_dict(compo.query.with_entities(elem.id_element, elem.libelle.label('libelle_elem'),
                                                     elem.type.label('type_elem'), elem.text.label('label_elem'),
                                                     elem.audio.label('audio_elem')).all())
