import logging

from model.shared_model import db, Cours, Apprenti, Assister
from custom_paquets.converter import convert_to_dict
from model.formation import get_formation_id, get_cours_par_formation


def get_all_cours(archive=False):
    """
    Retourne la liste de tous les cours

    :return: Une liste des cours
    """
    try:
        return convert_to_dict(Cours.query.with_entities(Cours.theme, Cours.cours, Cours.id_cours,
                                                       Cours.duree, Cours.id_formation).filter(
        Cours.archive == archive).all())
    except Exception as e:
        logging.error("Erreur lors de la récupération de tous les cours")
        logging.error(e)


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
        logging.error(f"Erreur lors de la récupération des apprentis de la formation {nom_formation}")
        logging.error(e)


def get_cours_par_apprenti(id_apprenti):
    """
    Retourne la liste de tous les cours auxquels un apprenti est inscrit

    :return: Une liste de cours
    """
    try:
        return convert_to_dict(Cours.query.with_entities(Cours.theme, Cours.cours, Cours.id_cours).join(Assister).filter_by(
            id_apprenti=id_apprenti).all())
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des cours de l'apprenti {id_apprenti}")
        logging.error(e)


def add_apprenti_assister(id_apprenti, id_formation):
    """
    Associe un apprenti à un cours en BD

    :return: None
    """
    try:
        cours = get_cours_par_formation(id_formation)
        for unCours in cours:
            assister = Assister(id_apprenti=id_apprenti, id_cours=unCours.id_cours)
            db.session.add(assister)
        db.session.commit()
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout de l'apprenti {id_apprenti} à la formation {id_formation}")
        logging.error(e)


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
    try:
        return Cours.query.with_entities(Cours.id_cours).filter_by(cours=nom_cours).first().id_cours
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'id du cours {nom_cours}")
        logging.error(e)
    

def get_nom_cours_by_id(id_cours):
    """
    Retourne le nom d'un cours à partir de son id

    :return: Un nom de cours
    """
    try:
        return Cours.query.with_entities(Cours.cours).filter_by(id_cours=id_cours).first().cours
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du nom du cours {id_cours}")
        logging.error(e)


def add_cours(theme, cours, duree, id_formation, commit=True):
    """
    Ajoute un cours en BD

    :return: id_cours
    """
    try:
        cours_ajoute = Cours(theme=theme, cours=cours, duree=duree, id_formation=id_formation)
        db.session.add(cours_ajoute)
        if commit:
            db.session.commit()
        return get_cours_id(cours)
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout du cours {cours}")
        logging.error(e)


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
        logging.error(f"Erreur lors de la modification du cours {intitule}")
        logging.error(e)


def archiver_cours(id_cours, archiver=True, commit=True):
    """
    Archive un cours en BD

    :return: un boolean (True si l'archivage s'est bien passé, False sinon)
    """
    try:
        cours = Cours.query.filter_by(id_cours=id_cours).first()
        cours.archive = archiver
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur lors de l'archivage du cours {id_cours}")
        logging.error(e)
        return False


def remove_cours(id_cours, commit=True):
    """
    Supprime un cours en BD

    :return: None
    """
    try:
        assister = Assister.query.filter_by(id_cours=id_cours).all()
        for a in assister:
            db.session.delete(a)
        if commit:
            db.session.commit()
        db.session.delete(Cours.query.filter_by(id_cours=id_cours).first())
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la suppression du cours {id_cours}")
        logging.error(e)
        return False