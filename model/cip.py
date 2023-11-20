from custom_paquets.converter import convert_to_dict
from model_db.trace import Trace


def get_commentaires_par_login_eleve(apprenti, id_fiche):
    """
    Recupere les commentaires d'une trace d'une fiche technique d'un apprenti à partir de son Login

    :return: Les informations de l'apprenti
    """
    return convert_to_dict(
        Trace.query.filter_by(login=apprenti, id_fiche = id_fiche).with_entities(Trace.commentaire_texte, Trace.commentaire_audio).all())
