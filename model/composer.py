from custom_paquets.converter import convert_to_dict
from model_db.ficheintervention import FicheIntervention
from model_db.elementbase import ElementBase
from model_db.composer import ComposerPresentation
from model_db.pictogramme import Pictogramme
from model_db.shared_model import db


def get_composer_presentation_dummy():
    return convert_to_dict(ComposerPresentation.query.filter_by(id_fiche=1).all())


def get_last_composer_presentation_by_login(login: str):
    return convert_to_dict(ComposerPresentation.query.filter_by(id_fiche=1).all())
