import logging

from flask import abort

from model.shared_model import db, Cours, Apprenti, Assister
from custom_paquets.converter import convert_to_dict
from model.formation import get_formation_id, get_cours_par_formation


def get_all_cours(archive=False):
    """
    Retourne la liste de tous les cours

    :return: Une liste des cours
    """
    return convert_to_dict(Cours.query.with_entities(Cours.theme, Cours.cours, Cours.id_cours,
                                                       Cours.duree, Cours.id_formation).filter(
        Cours.archive == archive).all())


def get_apprentis_by_formation(nom_formation: str, archive=False):
    """
    Retourne la liste de tous les apprentis inscrits à une formation

    :return: Une liste d'apprentis
    """
    try:
        return convert_to_dict(Cours.query.distinct().filter_by(id_formation=get_formation_id(nom_formation)).join(
            Assister).join(Apprenti).with_entities(Apprenti.nom, Apprenti.prenom, Apprenti.login,
                                                   Apprenti.photo).filter(Apprenti.archive == archive).all())
    except Exception as e:
        logging.error("Erreur lors de la récupération des apprentis par formation")
        logging.error(e)


def get_cours_par_apprenti(id_apprenti):
    """
    Retourne la liste de tous les cours auxquels un apprenti est inscrit

    :return: Une liste de cours
    """
    return convert_to_dict(Cours.query.with_entities(Cours.theme, Cours.cours, Cours.id_cours).join(Assister).filter_by(
        id_apprenti=id_apprenti).all())


def add_apprenti_assister(id_apprenti, id_formation):
    """
    Associe un apprenti à un cours en BD

    :return: None
    """
    cours = get_cours_par_formation(id_formation)
    for unCours in cours:
        assister = Assister(id_apprenti=id_apprenti, id_cours=unCours.id_cours)
        db.session.add(assister)
    db.session.commit()


def get_id_cours_by_theme(theme):
    """
    Retourne l'id d'un cours en fonction de son thème

    :return: id_cours
    """
    try:
        return Cours.query.filter_by(theme=theme).first().id_cours
    except Exception as e:
        logging.error("Erreur lors de la récupération de l'id du cours")
        logging.error(e)
        

def get_cours_id(nom_cours: str):
    """
    Retourne l'id d'un cours à partir de son nom

    :return: Un id de cours
    """
    return Cours.query.with_entities(Cours.id_cours).filter_by(cours=nom_cours).first().id_cours


def add_cours(theme, cours, duree, id_formation, commit=True):
    """
    Ajoute un cours en BD

    :return: id_cours
    """
    cours = Cours(theme=theme, cours=cours, duree=duree, id_formation=id_formation)
    db.session.add(cours)
    if commit:
        db.session.commit()
    return cours.id_cours


def update_cours(identifiant, theme, intitule, duree, id_formation, commit=True):
    """
    Modifie un cours en BD

    :return: None
    """
    try:
        cours = Cours.query.filter_by(id_cours = identifiant).first()
        cours.theme = theme
        cours.cours = intitule
        cours.duree = duree
        cours.id_formation = id_formation
        if commit:
            db.session.commit()
    except Exception as e:
        logging.error("Erreur lors de la modification du cours")
        logging.error(e)

