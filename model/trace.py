from custom_paquets.converter import convert_to_dict
from model_db.laissertrace import LaisserTrace
from model_db.ficheintervention import FicheIntervention
from model_db.shared_model import db



def get_commentaires_par_fiche(id_fiche):
    """
    Recupere les commentaires d'une trace d'une fiche technique d'un apprenti à partir de son Login

    :return: Les informations de l'apprenti
    """
    return convert_to_dict(
        LaisserTrace.query.filter_by(id_fiche=id_fiche).with_entities(LaisserTrace.commentaire_texte,
                                                                      LaisserTrace.intitule,
                                                                      LaisserTrace.eval_texte).all())


def modifier_commentaire_texte(id_personnel, horodatage, commentaire_texte):
    """
    Récupère le commentaire texte d'une fiche à partir de l'id du personnel et de son horodatage
    Modifie en DB la valeur du commentaire avec la nouvelle qui a été saisie par l'éducateur.
    
    :return: None
    """
    trace = LaisserTrace.query.filter_by(id_personnel = id_personnel, horodatage = horodatage).first()
    trace.commentaire_texte = commentaire_texte
    db.session.commit()


def modifier_evaluation_texte(id_personnel, horodatage, evaluation_texte):
    """
    Récupère l'évaluation texte d'une fiche à partir de l'id du personnel et de son horodatage
    Modifie en DB la valeur de l'éval avec la nouvelle qui a été saisie par l'éducateur.
    
    :return: None
    """
    trace = LaisserTrace.query.filter_by(id_personnel = id_personnel, horodatage = horodatage).first()
    trace.eval_texte = evaluation_texte
    db.session.commit()
