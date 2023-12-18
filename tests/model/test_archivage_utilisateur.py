from unidecode import unidecode
from model_db.apprenti import Apprenti
from model_db.personnel import Personnel
from model_db.shared_model import db

# Création d'un personnel à ajouter puis archiver
role="Educateur"
nom_personnel="Supreme"
prenom_personnel="Leader"
email="mail@mail.com"
pwd_personnel="000000".__hash__()
login_personnel=unidecode(prenom[0:2].upper().strip()) + unidecode(nom[0].upper().strip()) + str(
        len(nom.strip() + prenom.strip())).zfill(2)

# Création d'un apprenti à ajouter puis archiver
nom="SousFifre"
prenom="Malheureux"
photo="/url/photo.jpg"
login=unidecode(prenom[0:2].upper().strip()) + unidecode(nom[0].upper().strip()) + str(
        len(nom.strip() + prenom.strip())).zfill(2)

# Test d'archivage d'un apprenti
def test_archiver_apprenti(client):
    ## Copie du code dans add_personnel pour tester la fonction et éviter les commit() dans les tests
    personnel = Personnel(login = login, nom = nom, prenom = prenom, email = email, mdp = password, role = role)
    db.session.add(personnel)
    
    