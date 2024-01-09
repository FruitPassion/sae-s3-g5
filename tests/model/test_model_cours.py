from custom_paquets.tester_usages import CoursTest
from model.shared_model import Cours, db

def test_ajouter_cours(client):
    cours_t = CoursTest()
    
    # Récupération du cours à partir de son id
    cours = db.session.query(Cours).filter(Cours.id_cours == cours_t.id_cours).first()
    
    # Vérification que le cours existe
    assert cours is not None
    db.session.rollback()
    assert cours is None