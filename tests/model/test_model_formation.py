from custom_paquets.tester_usages import ApprentiTest, FormationTest
from model.formation import Formation
from model.apprenti import Apprenti
from model.cours import Cours
from model.shared_model import db


def test_ajouter_formation(client):
    formation_t = FormationTest()
    
    formation_d = db.session.query(Formation).filter(Formation.id_formation == formation_t.id_formation).first()
    assert formation_d is not None
    db.session.delete(formation_d)
    db.session.commit()
    assert db.session.query(Formation).filter(Formation.id_formation == formation_t.id_formation).first() is None


def test_archiver_formation(client):
    # Création d'une formation à archiver
    formation_t = FormationTest()

    Formation.archiver_formation(formation_t.id_formation, archiver=True, commit=False)
    assert db.session.query(Formation).filter(Formation.id_formation == formation_t.id_formation,
                                              Formation.archive == 1).first() is not None
    db.session.rollback()
    assert db.session.query(Formation).filter(Formation.id_formation == formation_t.id_formation,
                                              Formation.archive == 1).first() is None


def test_supprimer_formation(client):
    # Création d'une formation à supprimer
    formation = FormationTest()

    # Vérification de l'ajout de la formation
    assert db.session.query(Formation).filter(Formation.id_formation == formation.id_formation).first() is not None

    # Ajout d'un apprenti à la formation
    apprenti = ApprentiTest()

    # Ajout de l'apprenti dans un cours de la formation
    Cours.add_apprenti_assister(apprenti.id_apprenti, formation.id_formation)

    # Suppression de la formation
    Formation.remove_formation(formation.id_formation)

    # Vérification de la suppression de la formation dans la base de données
    assert db.session.query(Formation).filter(Formation.id_formation == formation.id_formation).first() is None

    # On vérifie qu'il n'y ait plus de session liée à la formation
    assert db.session.query(Cours).filter(Cours.id_formation == formation.id_formation).first() is None

    # Suppression de l'apprenti
    Apprenti.remove_apprenti(apprenti.id_apprenti)

    # Vérification de la suppression de l'apprenti en BD
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti.id_apprenti).first() is None
