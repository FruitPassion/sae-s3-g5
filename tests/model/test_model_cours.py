from custom_paquets.tester_usages import CoursTest
from model.shared_model import Cours, db

def test_ajouter_cours(client):
    cours_t = CoursTest()
    
    # Vérification que le cours existe
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours).first() is not None
    db.session.rollback()
    assert db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours).first() is None