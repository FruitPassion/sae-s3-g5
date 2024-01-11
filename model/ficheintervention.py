from datetime import date
from sqlalchemy import func, asc
from time import strftime, localtime

from custom_paquets.converter import convert_to_dict
from model.apprenti import get_id_apprenti_by_login, get_login_apprenti_by_id
from model.composer import get_composer_presentation
from model.personnel import get_id_personnel_by_login
from model.cours import get_nom_cours_by_id
from model.shared_model import db, FicheIntervention, ComposerPresentation, Apprenti


def get_fiches_techniques_par_login(login):
    """
    Récupère les identifiants des fiches techniques associées à un apprenti à partir de son Login

    :return: Les fiches techniques de l'apprenti
    """
    id_apprenti = get_id_apprenti_by_login(login)
    return convert_to_dict(FicheIntervention.query.filter_by(id_apprenti=id_apprenti).with_entities(
        FicheIntervention.id_fiche, FicheIntervention.etat_fiche, FicheIntervention.numero,
        FicheIntervention.date_creation, FicheIntervention.id_cours).order_by(asc(FicheIntervention.etat_fiche)).all())


def get_proprietaire_fiche_par_id_fiche(id_fiche):
    """
    Récupère le propriétaire d'une fiche à partir de son id

    :return: Le propriétaire de la fiche
    """
    return FicheIntervention.query.filter_by(id_fiche=id_fiche).join(Apprenti).with_entities(
        Apprenti.login).first().login


def get_fiches_par_id_fiche(id_apprenti):
    """
    Récupère les identifiants des fiches techniques associées à un apprenti à partir de son id

    :return: Les fiches techniques de l'apprenti
    """
    return convert_to_dict(FicheIntervention.query.filter_by(id_apprenti=id_apprenti).with_entities(
        FicheIntervention.id_fiche, FicheIntervention.numero).first())


def get_niveau_etat_fiches_par_login(login):
    """
    Récupère le total des niveaux de chaque fiche technique associées à un apprenti à partir de son Login

    :return: Les niveaux des fiches techniques de l'apprenti
    """
    id_apprenti = get_id_apprenti_by_login(login)
    fiche_niveau = (
        db.session.query(FicheIntervention.numero, func.sum(ComposerPresentation.niveau).label('total_niveau'), FicheIntervention.etat_fiche)
        .join(ComposerPresentation)
        .join(Apprenti)
        .filter(FicheIntervention.id_apprenti == id_apprenti)
        .filter(~ComposerPresentation.position_elem.like('%0%'))
        .group_by(FicheIntervention.id_fiche)
        .all()
    )
    return convert_to_dict(fiche_niveau)


def get_niveau_moyen_champs_par_login(login):
    """
    Récupère le niveau moyen des champs de chaque fiche technique associée à un apprenti à partir de son Login

    :return: Le niveau moyen des champs de chaque fiche technique de l'apprenti
    """
    id_apprenti = get_id_apprenti_by_login(login)
    niveau_champ = (
        db.session.query(FicheIntervention.numero, func.avg(ComposerPresentation.niveau).label('moyenne_niveau'))
        .join(ComposerPresentation)
        .join(Apprenti)
        .filter(FicheIntervention.id_apprenti == id_apprenti)
        .filter(~ComposerPresentation.position_elem.like('%0%'))
        .group_by(FicheIntervention.id_fiche)
        .all()
    )
    liste_niveau_champ = convert_to_dict(niveau_champ)
    total_niveau_champ = 0
    if len(liste_niveau_champ) == 0:
        return 0
    else:
        for niveau in liste_niveau_champ:
            total_niveau_champ += niveau["moyenne_niveau"]
        return int(total_niveau_champ / len(liste_niveau_champ))


def get_nombre_fiches_finies_par_login(login):
    """
    Récupère le nombre de fiches finies par un apprenti à partir de son Login

    :return: Les fiches techniques de l'apprenti
    """
    id_apprenti = get_id_apprenti_by_login(login)
    return FicheIntervention.query.filter_by(id_apprenti=id_apprenti).filter_by(etat_fiche=True).count()


def get_etat_fiche_par_id_fiche(id_fiche):
    """
    Récupère l'état d'une fiche à partir de son id

    :return: L'état de la fiche
    """
    return FicheIntervention.query.filter_by(id_fiche=id_fiche).with_entities(
        FicheIntervention.etat_fiche).first().etat_fiche

def get_fiches_techniques_finies_par_login(login):
    """
    Récupère les identifiants des fiches techniques associées à un apprenti à partir de son Login

    :return: Les fiches techniques de l'apprenti
    """
    id_apprenti = get_id_apprenti_by_login(login)
    return convert_to_dict(FicheIntervention.query.filter_by(id_apprenti=id_apprenti).with_entities(
        FicheIntervention.id_fiche, FicheIntervention.etat_fiche, FicheIntervention.numero,
        FicheIntervention.date_creation, FicheIntervention.id_cours).filter_by(etat_fiche=True).all())


def get_fiche_apprentis_existe(login: str):
    """
    Vérifie si l'apprenti a déjà une fiche

    :return: True s'il en a au moins une, False sinon
    """
    return FicheIntervention.query.filter_by(id_apprenti=get_id_apprenti_by_login(login)).count() != 0


def get_dernier_numero_fiche_apprenti(login: str):
    if get_fiche_apprentis_existe(login):
        return FicheIntervention.query.filter_by(id_apprenti=get_id_apprenti_by_login(login)).with_entities(
            FicheIntervention.numero).order_by(FicheIntervention.numero.desc()).first().numero
    else:
        return 0


def get_dernier_id_fiche_apprenti(login: str):
    """
    Récupère le dernier id de la fiche d'un apprenti

    :param login: login de l'apprenti
    :return: id de la fiche
    """

    if get_fiche_apprentis_existe(login):
        return FicheIntervention.query.filter_by(id_apprenti=get_id_apprenti_by_login(login)).with_entities(
            FicheIntervention.id_fiche).order_by(FicheIntervention.id_fiche.desc()).first().id_fiche
    else:
        return None


def copier_fiche(id_fiche: int, login_personnel: str):
    """
    A partir d'une fiche existante, la duplique et l'assigne a un apprenti

    :param id_fiche: id de la fiche à copier
    :param login_personnel: login du personnel
    :return: Code de validation en fonction du résultat
    """
    fiche_a_copier = FicheIntervention.query.filter_by(id_fiche=id_fiche).first()
    fiche_a_copier.etat_fiche = 2
    login_apprenti = get_login_apprenti_by_id(fiche_a_copier.id_apprenti)
    numero = get_dernier_numero_fiche_apprenti(login_apprenti) + 1
    nouvelle_fiche = FicheIntervention(numero=numero, nom_du_demandeur=fiche_a_copier.nom_du_demandeur,
                                       date_demande=fiche_a_copier.date_demande,
                                       localisation=fiche_a_copier.localisation,
                                       description_demande=fiche_a_copier.description_demande,
                                       degre_urgence=fiche_a_copier.degre_urgence,
                                       couleur_intervention=fiche_a_copier.couleur_intervention,
                                       etat_fiche=0, date_creation=strftime("%Y-%m-%d %H:%M:%S", localtime()),
                                       photo_avant=None, photo_apres=None,
                                       nom_intervenant=fiche_a_copier.nom_intervenant,
                                       prenom_intervenant=fiche_a_copier.prenom_intervenant,
                                       id_personnel=get_id_personnel_by_login(login_personnel),
                                       id_apprenti=get_id_apprenti_by_login(login_apprenti),
                                       id_cours=fiche_a_copier.id_cours)
    db.session.add(nouvelle_fiche)
    db.session.commit()
    composer_fiche = get_composer_presentation(id_fiche)
    for element in composer_fiche:
        element["id_fiche"] = nouvelle_fiche.id_fiche
        composer = ComposerPresentation(id_element=element["id_element"], id_fiche=element["id_fiche"],
                                        id_pictogramme=element["id_pictogramme"],
                                        taille_pictogramme=element["taille_pictogramme"],
                                        couleur_pictogramme=element["couleur_pictogramme"],
                                        text=None, taille_texte=element["taille_texte"], audio=None,
                                        police=element["police"], couleur=element["couleur"],
                                        couleur_fond=element["couleur_fond"], niveau=element["niveau"],
                                        position_elem=element["position_elem"],
                                        ordre_saisie_focus=element["ordre_saisie_focus"])
        db.session.add(composer)
    db.session.commit()
    return nouvelle_fiche.id_fiche


def assigner_fiche_dummy_eleve(login_apprenti: str, login_personnel: str, date_demande: date, nom_demandeur: str,
                               localisation: str, description_demande: str, degre_urgence: int,
                               couleur_intervention: str, nom_intervenant: str, prenom_intervenant: str, id_cours : str):
    """
    A partir de la fiche par defaut, la duplique et l'assigne a un apprenti

    :param login_apprenti: login de l'apprenti
    :param login_personnel: login du personnel
    :param date_demande: date de la demande
    :param nom_demandeur: nom du demandeur
    :param localisation: localisation de la demande
    :param description_demande: description de la demande
    :param degre_urgence: degré d'urgence de la demande
    :param couleur_intervention: couleur de l'intervention
    :param nom_intervenant: nom de l'intervenant
    :param prenom_intervenant: prénom de l'intervenant
    :param id_cours: id du cours
    :return: Code de validation en fonction du résultat
    """
    # Si l'apprenti a déjà une fiche, on copie les éléments de la dernière fiche
    if get_fiche_apprentis_existe(login_apprenti):
        composer_fiche = get_composer_presentation(get_dernier_id_fiche_apprenti(login_apprenti))
    # Sinon on copie les éléments de la fiche par défaut
    else:
        composer_fiche = get_composer_presentation()
    numero = get_dernier_numero_fiche_apprenti(login_apprenti) + 1
    nouvelle_fiche = FicheIntervention(numero=numero, nom_du_demandeur=nom_demandeur, date_demande=date_demande,
                                       localisation=localisation, description_demande=description_demande,
                                       degre_urgence=degre_urgence, couleur_intervention=couleur_intervention,
                                       etat_fiche=0, date_creation=strftime("%Y-%m-%d %H:%M:%S", localtime()),
                                       photo_avant=None, photo_apres=None, nom_intervenant=nom_intervenant,
                                       prenom_intervenant=prenom_intervenant,
                                       id_personnel=get_id_personnel_by_login(login_personnel),
                                       id_apprenti=get_id_apprenti_by_login(login_apprenti), id_cours=id_cours)
    db.session.add(nouvelle_fiche)
    db.session.commit()
    # On ajoute les éléments de la fiche
    for element in composer_fiche:
        element["id_fiche"] = nouvelle_fiche.id_fiche
        composer = ComposerPresentation(id_element=element["id_element"], id_fiche=element["id_fiche"],
                                        id_pictogramme=element["id_pictogramme"],
                                        taille_pictogramme=element["taille_pictogramme"],
                                        couleur_pictogramme=element["couleur_pictogramme"],
                                        text=None, taille_texte=element["taille_texte"], audio=None,
                                        police=element["police"], couleur=element["couleur"],
                                        couleur_fond=element["couleur_fond"], niveau=element["niveau"],
                                        position_elem=element["position_elem"],
                                        ordre_saisie_focus=element["ordre_saisie_focus"])
        db.session.add(composer)
    db.session.commit()

    return nouvelle_fiche.id_fiche
