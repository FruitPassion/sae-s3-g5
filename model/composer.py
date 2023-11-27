from custom_paquets.converter import convert_to_dict
from model_db.ficheintervention import FicheIntervention
from model_db.elementbase import ElementBase
from model_db.composer import ComposerPresentation as compo
from model_db.pictogramme import Pictogramme
from model_db.shared_model import db


def get_composer_presentation_dummy():
    return convert_to_dict(compo.query.filter_by(
        id_fiche=1).with_entities(compo.id_element, compo.taille_texte, compo.police, compo.couleur, compo.couleur_fond,
                                  compo.niveau, compo.position_elem, compo.ordre_saisie_focus).all())


def get_last_composer_presentation_by_login(last_fiche_id: int):
    return convert_to_dict(compo.query.filter_by(
        id_fiche=last_fiche_id).with_entities(compo.id_element, compo.taille_texte, compo.police, compo.couleur,
                                              compo.couleur_fond, compo.niveau, compo.position_elem,
                                              compo.ordre_saisie_focus).all())
