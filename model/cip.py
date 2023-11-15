from custom_paquets.converter import convertToDict
from model_db.apprenti import Apprenti
from model_db.trace import Trace


def getCommentairesParLoginEleve(apprenti):
    """
    Recupere les commentaires d'une trace d'une fiche technique d'un apprenti à partir de son Login

    :return: Les informations de l'apprenti
    """
    return convertToDict(Trace.query.filter_by(login=apprenti).with_entities(Trace.commentaire_texte, Trace.commentaire_audio).all())
