from datetime import datetime
import logging
from model.personnel import get_id_personnel_by_login
from model.shared_model import db, LaisserTrace


def get_commentaires_par_fiche(id_fiche):
    """
    Récupère les commentaires de la fiche id_fiche d'un apprenti

    :return: Tous les commentaires (évaluation texte et audio et commentaires audio et texte), leur horodatage
    et l'identifiant de l'éducateur ayant créé la trace
    """
    try:
        return LaisserTrace.query.filter_by(id_fiche=id_fiche).all()
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des commentaires de la fiche {id_fiche}")
        logging.error(e)


def get_commentaires_educ_par_fiche(id_fiche, apprenti="0"):
    
    """
    Récupère les commentaires de la fiche id_fiche d'un apprenti

    :return: Tous les commentaires (évaluation texte et audio et commentaires audio et texte), leur horodatage
    et l'identifiant de l'éducateur ayant créé la trace
    """
    try:
        return LaisserTrace.query.filter_by(id_fiche=id_fiche, apprenti=apprenti).first()
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des commentaires de la fiche {id_fiche}")
        logging.error(e)


def get_audio_commentaire(id_fiche):
    try:
        return LaisserTrace.query.filter_by(id_fiche=id_fiche).with_entities(LaisserTrace.audio).first().audio
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'audio {id_fiche}")
        logging.error(e)


def modifier_commentaire_texte(id_fiche, horodatage, commentaire_texte, typeCommentaire):
    """
    Récupère le commentaire audio du horodatage (date/heure) de la fiche id_fiche
    Modifie le commentaire textuel avec commentaire_texte

    :return: None
    """
    try:
        if typeCommentaire == "educateur":
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti="0").first()
            trace.commentaire_texte = commentaire_texte
            db.session.commit()
        else:
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti="1").first()
            print(commentaire_texte)
            trace.commentaire_texte = commentaire_texte
            db.session.commit()
    except Exception as e:
        logging.error(f"Erreur lors de la modification du commentaire textuel de la fiche {id_fiche} du {horodatage}")
        logging.error(e)


def modifier_commentaire_audio(id_fiche, horodatage, commentaire_audio, typeCommentaire):
    """
    Récupère le commentaire audio du horodatage (date/heure) de la fiche id_fiche
    Modifie le (chemin ?) commentaire audio  avec commentaire_audio
    :return: None
    """
    try:
        if typeCommentaire == "educateur":
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti="0").first()
            trace.commentaire_audio = commentaire_audio
        else:
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti="1").first()
            trace.commentaire_audio = commentaire_audio
        db.session.commit()
    except Exception as e:
        logging.error(f"Erreur lors de la modification du commentaire audio de la fiche {id_fiche} du {horodatage}")
        logging.error(e)


def modifier_evaluation_texte(id_fiche, horodatage, evaluation_texte, typeCommentaire):
    """
    Récupère l'évaluation textuelle du horodatage (date/heure) de la fiche id_fiche
    Modifie l'évaluation textuelle evaluation_texte avec evaluation_texte

    :return: None
    """
    try:
        if typeCommentaire == "educateur":
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti="0").first()
            trace.eval_texte = evaluation_texte
        else:
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti="1").first()
            trace.eval_texte = evaluation_texte
        db.session.commit()
    except Exception as e:
        logging.error(
            f"Erreur lors de la modification de l'évaluation textuelle de la fiche {id_fiche} du {horodatage}")
        logging.error(e)


def modifier_eval_audio(id_fiche, horodatage, eval_audio, typeCommentaire):
    """
    Récupère l'évaluation audio du horodatage (date/heure) de la fiche id_fiche
    Modifie (le chemin ?) l'évaluation audio eval_audio avec eval_audio

    :return: None
    """
    try:
        if typeCommentaire == "educateur":
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti="0").first()
            trace.eval_audio = eval_audio
        else:
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti="1").first()
            trace.eval_audio = eval_audio
        db.session.commit()
    except Exception as e:
        logging.error(f"Erreur lors de la modification de l'évaluation audio de la fiche {id_fiche} du {horodatage}")
        logging.error(e)


# jsp si ça marche malheureusement
def ajouter_commentaires_evaluation(id_fiche, commentaire_texte, eval_texte, commentaire_audio, eval_audio, login,
                                    intitule):
    """
    Ajoute les commentaires et évaluations d'une fiche technique d'un apprenti

    :return: None
    """
    try:
        id_personnel = get_id_personnel_by_login(login)
        horodatage = datetime.now()
        trace = LaisserTrace(id_fiche=id_fiche, id_personnel=id_personnel, horodatage=horodatage,
                             commentaire_texte=commentaire_texte, eval_texte=eval_texte,
                             commentaire_audio=commentaire_audio, eval_audio=eval_audio, apprenti="0",
                             intitule=intitule)
        db.session.add(trace)
        db.session.commit()
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout des commentaires et évaluations de la fiche {id_fiche}")
        logging.error(e)
