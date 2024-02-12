from custom_paquets.gestion_fichiers import vider_dossier
from custom_paquets.generation_xls import generer_xls_apprentis
from model.shared_model import db
import os


def test_ajouter_apprenti(client):
    folder = './static/files'
    
    # vider le dossier pour repartir à zero
    vider_dossier(folder)
    
    # Verifier que le dossier est bien vide
    assert len(os.listdir(folder)) == 0
    
    # Generation du fichier XLSX
    generer_xls_apprentis(1)
    
    # Verifier que le fichier à pu se générer sans soucis
    assert len(os.listdir(folder)) == 1
    
    