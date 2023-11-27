from datetime import date
from time import strftime, localtime

from custom_paquets.converter import convert_to_dict
from model.apprenti import get_id_apprenti_by_login
from model.composer import get_composer_presentation_dummy, get_last_composer_presentation_by_login
from model.personnel import get_id_personnel_by_login
from model_db.composer import ComposerPresentation
from model_db.ficheintervention import FicheIntervention
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
    return FicheIntervention.query.filter_by(id_apprenti=get_id_apprenti_by_login(login)).count != 0


def get_dernier_numero_fiche_apprenti(login: str):
    if get_fiche_apprentis_existe(login):
        return FicheIntervention.query.filter_by(id_apprenti=get_id_apprenti_by_login(login)).with_entities(
            FicheIntervention.numero).order_by(FicheIntervention.numero.desc()).first().numero
    else:
        return 0


def get_dernier_id_fiche_apprenti(login: str):
    if get_fiche_apprentis_existe(login):
        return FicheIntervention.query.filter_by(id_apprenti=get_id_apprenti_by_login(login)).with_entities(
            FicheIntervention.id_fiche).order_by(FicheIntervention.id_fiche.desc()).first().id_fiche
    else:
        return None


def assigner_fiche_dummy_eleve(login_apprenti: str, login_personnel: str, date_demande: date, nom_demandeur: str,
                               localisation: str, description_demande: str, degre_urgence: int,
                               couleur_intervention: str):
    """
    A partir de la fiche par defaut, la duplique et l'assigne a un eleve

    :return: Code de validation en fonction du résultat
    """
    dernier_fiche_id = get_dernier_id_fiche_apprenti(login_apprenti)
    numero = get_dernier_numero_fiche_apprenti(login_apprenti) + 1
    nouvelle_fiche = FicheIntervention(numero=numero, nom_du_demandeur=nom_demandeur, date_demande=date_demande,
                                       localisation=localisation, description_demande=description_demande,
                                       degre_urgence=degre_urgence, couleur_intervention=couleur_intervention,
                                       etat_fiche=0, date_creation=strftime("%Y-%m-%d %H:%M:%S", localtime()),
                                       photo_avant=None, photo_apres=None,
                                       id_personnel=get_id_personnel_by_login(login_personnel),
                                       id_apprenti=get_id_apprenti_by_login(login_apprenti))
    db.session.add(nouvelle_fiche)
    db.session.commit()
    if get_fiche_apprentis_existe(login_apprenti):
        composer_fiche = get_last_composer_presentation_by_login(dernier_fiche_id)
    else:
        composer_fiche = get_composer_presentation_dummy()
    for element in composer_fiche:
        element["id_fiche"] = nouvelle_fiche.id_fiche
        composer = ComposerPresentation(id_element=element["id_element"], id_fiche=element["id_fiche"], picto=None,
                                        text=None, taille_texte=element["taille_texte"], audio=None,
                                        police=element["police"], couleur=element["couleur"],
                                        couleur_fond=element["couleur_fond"], niveau=element["niveau"],
                                        position_elem=element["position_elem"],
                                        ordre_saisie_focus=element["ordre_saisie_focus"])
        db.session.add(composer)
    db.session.commit()
