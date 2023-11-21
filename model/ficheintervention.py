from custom_paquets.converter import convert_to_dict
from model.apprenti import get_id_apprenti_by_login
from model_db.ficheintervention import FicheIntervention


def get_fiches_techniques_par_login(login):
    """
    Récupère les identifiants des fiches techniques associées à un apprenti à partir de son Login

    :return: Les fiches techniques de l'apprenti
    """
    apprenti = get_id_apprenti_by_login(login)
    return convert_to_dict(FicheIntervention.query.filter_by(id_apprenti=apprenti["id_apprenti"]).with_entities(
        FicheIntervention.id_fiche).all())
