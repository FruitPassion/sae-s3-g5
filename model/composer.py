from custom_paquets.converter import convert_to_dict
from model.pictogramme import get_pictogramme_by_url
from model_db.shared_model import db, ComposerPresentation as Compo, ElementBase as Elem


def get_composer_presentation(id_fiche=1):
    """
    Permet de recuperer toutes les catégories d'une fiche

    :return: liste de dictionnaires
    """
    return convert_to_dict(
        Compo.query.filter_by(id_fiche=id_fiche).with_entities(Compo.id_element, Compo.id_pictogramme,
                                                               Compo.text, Compo.taille_texte,
                                                               Compo.police, Compo.taille_pictogramme,
                                                               Compo.couleur_pictogramme,
                                                               Compo.audio, Compo.police,
                                                               Compo.couleur, Compo.couleur_fond,
                                                               Compo.niveau,
                                                               Compo.position_elem,
                                                               Compo.ordre_saisie_focus).all())


def get_composer_categorie(id_fiche=1):
    """
    Permet de recuperer toutes les catégories d'une fiche

    :return: liste de dictionnaires
    """
    return convert_to_dict(Compo.query.filter_by(
        id_fiche=id_fiche).with_entities(Compo.id_element, Compo.id_pictogramme, Compo.text, Compo.taille_texte,
                                         Compo.police, Compo.audio, Compo.police, Compo.couleur, Compo.couleur_fond,
                                         Compo.niveau, Compo.position_elem, Compo.ordre_saisie_focus,
                                         Compo.taille_pictogramme, Compo.couleur_pictogramme).join(
        Elem).filter_by(type="categorie").all())


def get_composer_non_categorie(id_fiche=1):
    """
    Permet tous les elements d'une fiche associés à une catégorie

    :return: liste de dictionnaires
    """
    return convert_to_dict(
        db.session.query(Compo.id_element, Compo.text, Compo.taille_texte, Compo.police, Compo.audio, Compo.police,
                         Compo.couleur, Compo.couleur_fond, Compo.niveau, Compo.position_elem, Compo.taille_pictogramme,
                         Compo.ordre_saisie_focus, Compo.id_pictogramme.label("pictogramme"), Compo.taille_pictogramme,
                         Compo.couleur_pictogramme).filter_by(id_fiche=id_fiche).join(Elem).filter(Elem.type !=
                                                                                                   "categorie").all())


def get_elements_base():
    """
    Permet de recuprer les elements de base de la table ComposerPresentation

    :return: liste de dictionnaires avec l'id, le libelle, le type et l'url audio des elements
    """
    return convert_to_dict(Compo.query.with_entities(Elem.id_element, Elem.libelle.label('libelle_elem'),
                                                     Elem.type.label('type_elem'), Elem.text.label('label_elem'),
                                                     Elem.audio.label('audio_elem')).all())


def modifier_composition(form_data, id_fiche):
    compositions = Compo.query.filter_by(id_fiche=id_fiche).all()
    for composition in compositions:
        for key, value in form_data.items():
            if composition.position_elem == key.split('-')[-1] and "selecteur-element" not in key:
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
                    composition.id_pictogramme = get_pictogramme_by_url(value)["id_pictogramme"]
                elif 'taille-picto' in key:
                    composition.taille_pictogramme = value
                elif 'couleur-picto' in key:
                    composition.couleur_pictogramme = value
    db.session.commit()
