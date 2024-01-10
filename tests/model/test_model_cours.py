from custom_paquets.tester_usages import CoursTest, CoursTestModif
from model.cours import archiver_cours, remove_cours
from model.shared_model import Cours, Assister, db

def test_ajouter_cours(client):
    cours_t = CoursTest()
    
    # Vérification de l'ajout du cours
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours).first() is not None
    db.session.rollback()
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours).first() is None

def test_modifier_cours(client):
    cours_t = CoursTest()

    cours_m = CoursTestModif(cours_t.id_cours)
    
    # Vérification de la modification du cours
    cours_modif: Cours = db.session.query(Cours).filter(Cours.id_cours == cours_m.id_cours).first()
    assert cours_modif is not None
    assert cours_modif.theme == cours_m.theme
    assert cours_modif.cours == cours_m.cours
    assert cours_modif.duree == cours_m.duree
    assert cours_modif.id_formation == cours_m.id_formation

    db.session.rollback()
    
def test_archiver_cours(client):
    cours_t = CoursTest()

    archiver_cours(cours_t.id_cours, archiver=True, commit=False)
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours, Cours.archive == 1).first() is not None
    db.session.rollback()
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours, Cours.archive == 1).first() is None
    
def test_supprimer_cours(client):
    cours_t = CoursTest(commit=True)
    
    # Vérification de l'ajout du cours
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours).first() is not None
    
    # Suppression du cours
    remove_cours(cours_t.id_cours)
    
    # Vérification de la suppression du cours dans la base de données
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours).first() is None
    assert db.session.query(Assister).filter(Assister.id_cours == cours_t.id_cours).first() is None