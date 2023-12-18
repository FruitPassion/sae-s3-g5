from flask import abort

from model_db.shared_model import db, Session, Apprenti, Assister
from custom_paquets.converter import convert_to_dict
from model.formation import get_formation_id, get_sessions_par_formation


def get_all_sessions(archive=False):
    """
    Retourne la liste de toutes les sessions

    :return: Une liste des sessions
    """
    return convert_to_dict(Session.query.with_entities(Session.theme, Session.cours, Session.id_session,
                                                       Session.duree, Session.id_formation).filter(
        Session.archive == archive).all())


def get_apprentis_by_formation(nom_formation: str, archive=False):
    """
    Retourne la liste de tous les apprentis inscrits à une formation

    :return: Une liste d'apprentis
    """
    try:
        return convert_to_dict(Session.query.distinct().filter_by(id_formation=get_formation_id(nom_formation)).join(
            Assister).join(Apprenti).with_entities(Apprenti.nom, Apprenti.prenom, Apprenti.login,
                                                   Apprenti.photo).filter(Apprenti.archive == archive).all())
    except:
        abort(404)


def add_apprenti_assister(id_apprenti, id_formation):
    """
    Associe un apprenti à une session en BD

    :return: None
    """
    sessions = get_sessions_par_formation(id_formation)
    for session in sessions:
        assister = Assister(id_apprenti=id_apprenti, id_session=session.id_session)
        db.session.add(assister)
    db.session.commit()
