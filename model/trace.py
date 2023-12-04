from datetime import datetime
from custom_paquets.converter import convert_to_dict
from model.personnel import get_id_personnel_by_login
from model_db.laissertrace import LaisserTrace
from model_db.ficheintervention import FicheIntervention
from model_db.shared_model import db


def get_commentaires_par_fiche(id_fiche):
    """
    Recupere les commentaires d'une trace d'une fiche technique d'un apprenti à partir de son Login

    :return: Les informations de l'apprenti
    """
    return convert_to_dict(
        LaisserTrace.query.filter_by(
            id_fiche=id_fiche).with_entities(LaisserTrace.commentaire_texte, LaisserTrace.intitule,
                                             LaisserTrace.eval_texte, LaisserTrace.horodatage,
                                             LaisserTrace.commentaire_audio, LaisserTrace.eval_audio,
                                             LaisserTrace.id_personnel).all())


def get_commentaires_educ_par_fiche(id_fiche):
    """
    Recupere les commentaires d'une trace d'une fiche technique d'un apprenti à partir de son Login

    :return: Les informations de l'apprenti
    """
    return convert_to_dict(
        LaisserTrace.query.filter_by(id_fiche=id_fiche, apprenti="0"
                                     ).with_entities(LaisserTrace.commentaire_texte, LaisserTrace.intitule,
                                                     LaisserTrace.eval_texte, LaisserTrace.horodatage,
                                                     LaisserTrace.commentaire_audio, LaisserTrace.eval_audio,
                                                     LaisserTrace.id_personnel).first())


def modifier_commentaire_texte(id_fiche, horodatage, commentaire_texte):
    """
    Récupère le commentaire texte d'une fiche à partir de l'id du personnel et de son horodatage
    Modifie en DB la valeur du commentaire avec la nouvelle qui a été saisie par l'éducateur.
    
    :return: None
    """

    trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage).first()
    trace.commentaire_texte = commentaire_texte
    db.session.commit()


def modifier_commentaire_audio(id_fiche, horodatage, commentaire_audio):
    """
    Récupère le commentaire texte d'une fiche à partir de l'id du personnel et de son horodatage
    Modifie en DB la valeur du commentaire avec la nouvelle qui a été saisie par l'éducateur.
    
    :return: None
    """
    trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage).first()
    trace.commentaire_audio = commentaire_audio
    db.session.commit()


def modifier_evaluation_texte(id_fiche, horodatage, evaluation_texte):
    """
    Récupère l'évaluation texte d'une fiche à partir de l'id du personnel et de son horodatage
    Modifie en DB la valeur de l'éval avec la nouvelle qui a été saisie par l'éducateur.
    
    :return: None
    """
    trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage).first()
    trace.eval_texte = evaluation_texte
    db.session.commit()


def modifier_eval_audio(id_fiche, horodatage, eval_audio):
    """
    Récupère le commentaire texte d'une fiche à partir de l'id du personnel et de son horodatage
    Modifie en DB la valeur du commentaire avec la nouvelle qui a été saisie par l'éducateur.
    
    :return: None
    """
    trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage).first()
    trace.eval_audio = eval_audio
    db.session.commit()

# jsp si ça marche malheureusement
def ajouter_commentaires_evaluation(id_fiche, commentaire_texte, eval_texte, commentaire_audio, eval_audio):
    """
    Ajoute les commentaires et évaluations d'une fiche technique d'un apprenti

    :return: None
    """
    id_personnel = get_id_personnel_by_login()
    fiche = FicheIntervention.query.filter_by(id_fiche=id_fiche).first()
    horodatage = datetime.now()
    trace = LaisserTrace(id_fiche=fiche.id_fiche, id_personnel=id_personnel, horodatage=horodatage,
                         commentaire_texte=commentaire_texte, eval_texte=eval_texte, commentaire_audio=commentaire_audio,eval_audio=eval_audio, intitule=fiche.intitule)
    db.session.add(trace)
    db.session.commit()