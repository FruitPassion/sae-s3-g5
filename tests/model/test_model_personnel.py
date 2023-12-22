from custom_paquets.tester_usages import PersonnelTest, PersonnelTestModif
from model.personnel import  get_id_personnel_by_login, archiver_personnel
from model.shared_model import Personnel, db


# Test de l'ajout d'un personnel
def test_ajouter_personnel(client):
    personnel = PersonnelTest()

    assert db.session.query(Personnel).filter(Personnel.login == personnel.login).first() is not None
    db.session.rollback()
    assert db.session.query(Personnel).filter(Personnel.login == personnel.login).first() is None


# Test d'archivage d'un personnel
def test_archiver_personnel(client):
    # Création d'un personnel à ajouter puis archiver
    personnel = PersonnelTest()

    # Archivage du personnel
    archiver_personnel(personnel.id_personnel, archiver=True, commit=False)

    # Vérification que le personnel a bien été archivé
    assert db.session.query(Personnel).filter(Personnel.id_personnel == personnel.id_personnel,
                                              Personnel.archive == 1).first() is not None
    db.session.rollback()
    assert db.session.query(Personnel).filter(Personnel.id_personnel == personnel.id_personnel,
                                              Personnel.archive == 1).first() is None


def test_modifier_personnel(client):
    # Création d'un personnel à ajouter puis archiver
    personnel = PersonnelTest()

    # Modification de tous les champs du personnel
    personnel2 = PersonnelTestModif(personnel.id_personnel)

    # Vérification que le personnel a bien été modifié
    mysession = db.session()
    mysession.autoflush = False
    with mysession.no_autoflush:
        personnel_modif = Personnel.query.filter_by(id_personnel=personnel2.id_personnel).first()
        assert personnel_modif is not None
        assert personnel_modif.nom == personnel2.nom
        assert personnel_modif.prenom == personnel2.prenom
        assert personnel_modif.login == personnel2.login
        assert personnel_modif.email == personnel2.email

    db.session.rollback()
