from datetime import date
from time import strftime, localtime

from custom_paquets.converter import convert_to_dict
from model.apprenti import get_id_apprenti_by_login
from model.composer import get_composer_presentation_dummy
from model.personnel import get_id_personnel_by_login
from model_db.composer import ComposerPresentation
from model_db.ficheintervention import FicheIntervention
from model_db.formation import Formation
from model_db.shared_model import db


def get_fiches_techniques_par_login(login):
    """
    Récupère les identifiants des fiches techniques associées à un apprenti à partir de son Login

    :return: Les fiches techniques de l'apprenti
    """
    id_apprenti = get_id_apprenti_by_login(login)
    return convert_to_dict(FicheIntervention.query.filter_by(id_apprenti=id_apprenti).with_entities(
        FicheIntervention.id_fiche, FicheIntervention.etat_fiche).all())


def get_fiches_techniques_finies_par_login(login):
    """
    Récupère les identifiants des fiches techniques associées à un apprenti à partir de son Login

    :return: Les fiches techniques de l'apprenti
    """
    id_apprenti = get_id_apprenti_by_login(login)
    return convert_to_dict(FicheIntervention.query.filter_by(id_apprenti=id_apprenti).with_entities(
        FicheIntervention.id_fiche, FicheIntervention.etat_fiche).filter_by(etat_fiche=True).all())


def get_fiche_apprentis_existe(login: str):
    """
    Verifie si l'apprenti à deja une fiche

    :return: Boolean, vrai si il en a faux sinon
    """


def get_dernier_numero_fiche_apprenti(login: str):
    try:
        return FicheIntervention.query.filter_by(id_apprenti=get_id_apprenti_by_login(login)).with_entities(
            FicheIntervention.numero).order_by(FicheIntervention.numero.desc()).first().numero
    except:
        return 0


def assigner_fiche_dummy_eleve(login_apprenti: str, login_personnel: str, date_demande: date, nom_demandeur: str,
                               localisation: str, description_demande: str, degre_urgence: int,
                               couleur_intervention: str):
    """
    A partir de la fiche par defaut, la duplique et l'assigne a un eleve

    :return: Code de validation en fonction du résultat
    """
    numero = get_dernier_numero_fiche_apprenti(login_apprenti) + 1
    nouvelle_fiche = FicheIntervention(numero, nom_demandeur, date_demande, localisation, description_demande,
                                       degre_urgence, couleur_intervention, 0,
                                       strftime("%Y-%m-%d %H:%M:%S", localtime()), None, None,
                                       get_id_personnel_by_login(login_personnel),
                                       get_id_apprenti_by_login(login_apprenti))
    db.session.add(nouvelle_fiche)
    db.session.commit()
    db.refresh(nouvelle_fiche)
    composer_dummy = get_composer_presentation_dummy()
    for element in composer_dummy:
        element["id_fiche"] = nouvelle_fiche.id_fiche
        composer = ComposerPresentation(element["id_element"], element["id_fiche"], element["picto"],
                                                  element["text"], element["taille_texte"], element["audio"],
                                                  element["police"], element["couleur"], element["couleur_fond"])
        db.session.add(composer)
    db.session.commit()
