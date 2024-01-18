import logging, sys, os
from custom_paquets.converter import convert_to_dict
from custom_paquets.gestions_erreur import suplement_erreur
from model.pictogramme import get_pictogramme_by_url
from model.shared_model import db, ComposerPresentation as Compo, ElementBase as Elem


def get_composer_presentation(id_fiche=1):
    """
    Permet de récupérer tous les éléments d'une fiche

    :return: liste de dictionnaires
    """
    try:
        return Compo.query.filter_by(id_fiche=id_fiche).all()
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de la récupération des éléments de la fiche.")


def get_composer_categorie(id_fiche=1):
    """
    Permet de récupérer toutes les catégories d'une fiche

    :return: liste de dictionnaires
    """
    try:
        return convert_to_dict(Compo.query.filter_by(id_fiche=id_fiche).join(Elem).filter_by(type="categorie").all())
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de la récupération des catégories de la fiche.")


def get_composer_non_categorie(id_fiche=1):
    """
    Permet de récupérer tous les éléments d'une fiche associés à une catégorie

    :return: liste de dictionnaires
    """
    try:
        return convert_to_dict(
            Compo.query.with_entities(Compo.id_element, Compo.text, Compo.taille_texte, Compo.police, Compo.audio,
                                      Compo.police, Compo.couleur, Compo.couleur_fond, Compo.niveau,
                                      Compo.position_elem,
                                      Compo.taille_pictogramme, Compo.ordre_saisie_focus,
                                      Compo.id_pictogramme.label("pictogramme"), Compo.taille_pictogramme,
                                      Compo.couleur_pictogramme, Compo.id_materiel).filter_by(
                id_fiche=id_fiche).join(Elem).filter(Elem.type != "categorie").all())
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de la récupération des éléments de la fiche.")


def get_elements_base():
    """
    Permet de récupérer les éléments de base de la table ComposerPresentation

    :return: liste de dictionnaires avec l'id, le libellé, le type et l'url audio des éléments
    """
    try:
        return convert_to_dict(Compo.query.with_entities(Elem.id_element, Elem.libelle.label('libelle_elem'),
                                                         Elem.type.label('type_elem'), Elem.text.label('label_elem'),
                                                         Elem.audio.label('audio_elem')).all())
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de la récupération des éléments de base.")


def modifier_composition(form_data, id_fiche):
    try:
        compositions = Compo.query.filter_by(id_fiche=id_fiche).all()
        for composition in compositions:
            for key, value in form_data.items():
                if composition.position_elem == key.split('-')[-1] and "selecteur-element" not in key:
                    modifier_composition_par_element(composition, key, value)
        db.session.commit()
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de la modification de la composition de la fiche.")


def modifier_composition_par_element(composition, key, value):
    try:
        if 'selecteur-niveau' in key:
            composition.niveau = value
        elif 'selecteur-police' in key:
            composition.police = value
        elif 'taille-police' in key:
            composition.taille_texte = value
        elif 'couleur-police' in key:
            composition.couleur = value
        elif 'couleur-fond' in key:
            composition.couleur_fond = value
        elif 'selecteur-picto' in key:
            composition.id_pictogramme = get_pictogramme_by_url(value).id_pictogramme
        elif 'taille-picto' in key:
            composition.taille_pictogramme = value
        elif 'couleur-picto' in key:
            composition.couleur_pictogramme = value

    except Exception as e:
        suplement_erreur(e, message="Erreur lors de la modification de la composition de la fiche.")


def maj_materiaux_fiche(majs: dict, id_fiche: str):
    """
    Permet de mettre à jour les matériaux d'une fiche

    :param majs: dictionnaire contenant les matériaux à mettre à jour
    :param id_fiche: id de la fiche à mettre à jour
    :return: None
    """
    try:
        compositions = Compo.query.filter_by(id_fiche=id_fiche).all()
        for element in compositions:
            if element.position_elem in majs.keys():
                element.id_materiel = majs[f'{element.position_elem}']
        db.session.commit()
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de l'enregistrement des modifications de la fiche.")


def maj_contenu_fiche(majs: dict, id_fiche: str):
    """
    Permet de mettre à jour le contenu d'une fiche

    :param majs: dictionnaire contenant les éléments à mettre à jour
    :param id_fiche: id de la fiche à mettre à jour
    :return:
    """
    try:
        compositions = Compo.query.filter_by(id_fiche=id_fiche).all()
        for element in compositions:
            if element.position_elem in majs.keys():
                element.text = majs[f'{element.position_elem}']
        db.session.commit()
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de l'enregistrement des modifications de la fiche.")


def get_composer_presentation_par_apprenti(id_fiche):
    """
    Permet de récupérer ce que l'apprenti a complété dans une fiche
    """
    try:
        return db.session.query(Compo).filter_by(id_fiche=id_fiche).join(Elem).all()
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de la récupération des éléments de la fiche.")


def get_checkbox_on(id_fiche):
    """
    Permet de récupérer les checkbox cochées de la fiche

    :param id_fiche:
    :return:
    """
    try:
        return Compo.query.filter_by(text="on", id_fiche=id_fiche).all()
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de la récupération des checkbox de la fiche.")


def get_radio_radioed(id_fiche):
    """
    Permet de récupérer les radios cochées de la fiche

    :param id_fiche:
    :return:
    """
    try:
        return Compo.query.filter_by(text="radioed", id_fiche=id_fiche).all()
    except Exception as e:
        suplement_erreur(e, message="Erreur lors de la récupération des radios de la fiche.")
