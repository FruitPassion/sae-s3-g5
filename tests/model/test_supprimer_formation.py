from custom_paquets.converter import generate_login
from model.apprenti import add_apprenti, get_id_apprenti_by_login, remove_apprenti
from model.formation import get_formation_id, remove_formation, add_formation
from model.session import add_apprenti_assister, get_sessions_par_formation
from model.shared_model import Apprenti, db, Formation, Session

def test_supprimer_formation(client):
    ## Création d'une formation à supprimer
    intitule = "Parcours électricité"
    niveau_qualification = 3
    groupe = "3"
    image = "formation_image/elec.jpg"

    # ajout de la formation
    add_formation(intitule, niveau_qualification, groupe, image)

    # vérification que la formation soit bien dans la base de données
    assert db.session.query(Formation).filter(Formation.intitule == intitule).first() is not None

    id_formation = get_formation_id(intitule)

    ## Ajout d'un apprenti à la formation
    nom_apprenti = "SousFifre"
    prenom_apprenti = "Malheureux"
    photo = "/url/photo.jpg"
    login_apprenti = generate_login(nom_apprenti, prenom_apprenti)
    
    # ajout de l'apprenti
    add_apprenti(nom_apprenti, prenom_apprenti, login_apprenti, photo)
    
    id_apprenti = get_id_apprenti_by_login(login_apprenti)
    
    # Ajout de l'apprenti dans une session de la formation
    add_apprenti_assister(id_apprenti, id_formation)
    
    # Suppression de la formation
    remove_formation(id_formation, commit=True)

    # vérification que la formation soit bien supprimée de la base de données
    assert db.session.query(Formation).filter(Formation.intitule == intitule).first() is None
    
    # Vérification qu'il n'y ait plus de session liée à la formation
    assert db.session.query(Session).filter(Session.id_formation == id).first() is None
    
    # Suppression de l'apprenti
    remove_apprenti(id_apprenti)
    
    # Vérification que l'apprenti soit bien supprimé de la base de données
    assert db.session.query(Apprenti).filter(Apprenti.id_apprenti == id_apprenti).first() is None