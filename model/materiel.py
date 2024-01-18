from custom_paquets.gestions_erreur import suplement_erreur
from model.shared_model import Materiel, db

def get_all_materiel():
    """
    Récupère tout le matériel

    :return: liste de tous les matériels
    """
    return Materiel.query.all()


def add_materiel(nom, categorie, lien, commit=True):
    """
    Ajoute un matériel en BD

    """
    try:
        materiel = Materiel(nom=nom, categorie = categorie, lien=lien)
        db.session.add(materiel)
        if commit:
            db.session.commit()

    except Exception as e:
        suplement_erreur(e, message=f"Erreur lors de l'ajout du matériel {nom} dans la catégorie {categorie}")


def update_materiel(identifiant, nom, categorie, lien, commit=True):
    """
    Ajoute un matériel en BD

    """
    try:
        materiel = Materiel.query.filter_by(id_materiel = identifiant).first()
        materiel.nom = nom
        materiel.categorie = categorie
        materiel.lien = lien
        if commit:
            db.session.commit()

    except Exception as e:
        suplement_erreur(e, message=f"Erreur lors de la modification du matériel {nom}")


def get_photo_materiel(id_materiel):
    try:
        return Materiel.query.filter_by(id_materiel=id_materiel).with_entities(Materiel.lien).first().lien
    except Exception as e:
        suplement_erreur(e, message=f"Erreur lors de la récupération du lien de la photo du matériel {id_materiel}.")
