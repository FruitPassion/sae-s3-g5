from custom_paquets.tester_usages import ApprentiTest, ApprentiTestModif
from model.apprenti import archiver_apprenti, remove_apprenti
from model.shared_model import Apprenti, db, FicheIntervention


def test_ajouter_apprenti(client):
    apprenti = ApprentiTest()

    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti.id_apprenti).first() is not None
    db.session.rollback()
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti.id_apprenti).first() is None


# Test d'archivage d'un apprenti
def test_archiver_apprenti(client):
    apprenti = ApprentiTest()

    archiver_apprenti(apprenti.id_apprenti, archiver=True, commit=False)
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti.id_apprenti,
                                             Apprenti.archive == 1).first() is not None
    db.session.rollback()
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti.id_apprenti,
                                             Apprenti.archive == 1).first() is None


def test_modifier_apprenti(client):
    # Création d'un apprenti à modifier
    apprenti = ApprentiTest()

    # Modification de l'apprenti
    apprenti2 = ApprentiTestModif(apprenti.id_apprenti)

    # Vérification de la modification de l'apprenti
    apprenti_modif: Apprenti = db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti2.id_apprenti).first()
    assert apprenti_modif is not None
    assert apprenti_modif.nom == apprenti2.nom
    assert apprenti_modif.prenom == apprenti2.prenom
    assert apprenti_modif.login == apprenti2.login
    assert apprenti_modif.photo == apprenti2.photo

    db.session.rollback()


def test_supprimer_apprenti(client):
    # Création d'un apprenti à modifier
    apprenti = ApprentiTest()

    remove_apprenti(apprenti.id_apprenti)
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti.id_apprenti).first() is None
    assert len(FicheIntervention.query.filter_by(id_apprenti=apprenti.id_apprenti).all()) == 0
