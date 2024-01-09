from custom_paquets.tester_usages import ApprentiTest, FormationTest
from model.formation import archiver_formation
from model.apprenti import remove_apprenti
from model.formation import remove_formation
from model.cours import add_apprenti_assister
from model.shared_model import Apprenti, db, Formation, Cours


def test_ajouter_formation(client):
    formation_t = FormationTest()

    assert db.session.query(Formation).filter(Formation.id_formation == formation_t.id_formation).first() is not None
    db.session.rollback()
    assert db.session.query(Formation).filter(Formation.id_formation == formation_t.id_formation).first() is None


def test_archiver_formation(client):
    # Création d'une formation à archiver
    formation_t = FormationTest()

    archiver_formation(formation_t.id_formation, archiver=True, commit=False)
    assert db.session.query(Formation).filter(Formation.id_formation == formation_t.id_formation,
                                              Formation.archive == 1).first() is not None
    db.session.rollback()
    assert db.session.query(Formation).filter(Formation.id_formation == formation_t.id_formation,
                                              Formation.archive == 1).first() is None


def test_supprimer_formation(client):
    # Création d'une formation à supprimer
    formation = FormationTest(commit=True)

    # vérification que la formation soit bien dans la base de données
    assert db.session.query(Formation).filter(Formation.id_formation == formation.id_formation).first() is not None

    # Ajout d'un apprenti à la formation
    apprenti = ApprentiTest(commit=True)

    # Ajout de l'apprenti dans un cours de la formation
    add_apprenti_assister(apprenti.id_apprenti, formation.id_formation)

    # Suppression de la formation
    remove_formation(formation.id_formation)

    # vérification que la formation soit bien supprimée de la base de données
    assert db.session.query(Formation).filter(Formation.id_formation == formation.id_formation).first() is None

    # Vérification qu'il n'y ait plus de session liée à la formation
    assert db.session.query(Cours).filter(Cours.id_formation == formation.id_formation).first() is None

    # Suppression de l'apprenti
    remove_apprenti(apprenti.id_apprenti)

    # Vérification que l'apprenti soit bien supprimé de la base de données
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti.id_apprenti).first() is None
