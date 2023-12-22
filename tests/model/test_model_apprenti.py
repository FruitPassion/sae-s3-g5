from custom_paquets.converter import generate_login
from custom_paquets.security import encrypt_password
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

    # Modification des chmaps de l'apprenti
    new_nom = "Du Maître"
    new_prenom = "Toutou"
    new_login = generate_login(new_nom, new_prenom)
    new_photo = "/url/photo2.jpg"
    password = encrypt_password("121212")

    # Modification de l'apprenti
    apprenti2 = ApprentiTestModif(apprenti.id_apprenti)

    # Vérification que l'apprenti soit bien modifé
    apprenti_modif: Apprenti = db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti2.id_apprenti).first()
    assert apprenti_modif is not None
    assert apprenti_modif.nom == new_nom
    assert apprenti_modif.prenom == new_prenom
    assert apprenti_modif.login == new_login
    assert apprenti_modif.photo == new_photo
    assert apprenti_modif.photo == new_photo

    db.session.rollback()


def test_supprimer_apprenti(client):
    # Création d'un apprenti à modifier
    apprenti = ApprentiTest()

    remove_apprenti(apprenti.id_apprenti)
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == apprenti.id_apprenti).first() is None
    assert len(FicheIntervention.query.filter_by(id_apprenti=apprenti.id_apprenti).all()) == 0
