from custom_paquets import gestion_image
from PIL import ImageColor

def test_ajouter_apprenti(client):
    couleur = gestion_image.random_color()
    
    # verifier que une couleur est bien générée 
    assert couleur in dict(ImageColor.colormap).keys()
    
    # vérifier que la couleur n'est pas interdite
    assert couleur not in ["black", "white", "lightgrey", "darkgrey", "grey", "dimgrey", "dimgray", "silver", "gainsboro"]
    
    
