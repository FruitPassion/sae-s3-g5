from custom_paquets.converter import convert_to_dict
from model_db.laissertrace import LaisserTrace
from model_db.ficheintervention import FicheIntervention


def get_commentaires_par_fiche(id_fiche):
    """
    Recupere les commentaires d'une trace d'une fiche technique d'un apprenti à partir de son Login

    :return: Les informations de l'apprenti
    """
    return convert_to_dict(
        LaisserTrace.query.filter_by(id_fiche=id_fiche).with_entities(LaisserTrace.commentaire_texte,
                                                                      LaisserTrace.intitule,
                                                                      LaisserTrace.eval_texte).all())
