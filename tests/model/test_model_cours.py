from custom_paquets.tester_usages import CoursTest, CoursTestModif
from model.shared_model import Cours, db

def test_ajouter_cours(client):
    cours_t = CoursTest()
    
    # Vérification que le cours existe
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours).first() is not None
    db.session.rollback()
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours).first() is None

def test_modifier_cours(client):
    cours_t = CoursTest()

    cours_m = CoursTestModif(cours_t.id_cours)
    
    # Vérification que le cours soit bien modifé
    cours_modif: Cours = db.session.query(Cours).filter(Cours.id_cours == cours_m.id_cours).first()
    assert cours_modif is not None
    assert cours_modif.theme == cours_m.theme
    assert cours_modif.cours == cours_m.cours
    assert cours_modif.duree == cours_m.duree
    assert cours_modif.id_formation == cours_m.id_formation

    db.session.rollback()