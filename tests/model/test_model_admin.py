from unidecode import unidecode
from model_db.personnel import Personnel
from model_db.shared_model import db

# Test de l'ajout d'un personnel
def test_ajouter_personnel():
    role="Educateur"
    nom="Supreme"
    prenom="Leader"
    email="mail@mail.com"
    password="000000".__hash__()
    login=unidecode(prenom[0:2].upper().strip()) + unidecode(nom[0].upper().strip()) + str(
            len(nom.strip() + prenom.strip())).zfill(2)
    
    ## Copie du code dans add_personnel pour tester la fonction et éviter les commit() dans les tests
    personnel = Personnel(login = login, nom = nom, prenom = prenom, email = email, mdp = password, role = role)
    db.session.add(personnel)
    
    assert db.session.query(Personnel).filter(Personnel.login == "LES13").first() is not None
    db.session.rollback()
    assert db.session.query(Personnel).filter(Personnel.login == "LES13").first() is None
    
# Test de l'ajout d'un apprenti (mais la fonction est dans le model apprenti ??)
