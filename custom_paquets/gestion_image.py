import os
from PIL import Image, ImageFilter, ImageOps, ImageColor
from werkzeug.utils import secure_filename
from random import randint
from model.shared_model import db
import secrets
import numpy as np
import cv2
from matplotlib import colors

def img_estim(img, thrshld):
    is_light = np.mean(img) > thrshld
    return 'light' if is_light else 'dark'

def random_color(pixel):
    color_for_dark = ["lightcoral", "mistyrose", "peachpuff", "bisque", "papayawhip", "oldlace",
                      "cornsilk", "palegreen", "lightgreen", "palegoldenrod", "azure", "lightcyan", "paleturquoise", "lavender", "powderblue", "lightblue", "skyblue", "lightskyblue", "aliceblue",
                      "lightsteelblue", "thistle", "lavenderblush", "plum", "lightpink", "pink", "lightcoral", "salmon", "lightsalmon", "sandybrown"]
    
    color_for_light = ["brown", "firebrick", "sienna", "chocolate", "peru", "burlywood", "tan", "goldenrod",
                       "gold", "darkkhaki", "olive", "olivedrab", "yellowgreen", "forestgreen", "green",
                       "seagreen", "mediumseagreen", "mediumaquamarine", "lightseagreen", "teal",
                       "cadetblue", "deepskyblue", "steelblue", "cornflowerblue", "royalblue", "slateblue",
                       "mediumpurple", "darkorchid", "mediumorchid", "hotpink", "mediumvioletred", "palevioletred"]
    if pixel == 'light':
        return secrets.choice(color_for_light)
    else:
        return secrets.choice(color_for_dark)
    
def to_rgb255(tuple_color):
    rgb_color = tuple(int(x * 255) for x in tuple_color)
    return rgb_color

def resize_image_profile(img: Image, path: str):
    img_width, img_height = img.size
    if img.size[0] < img.size[1]:
        crop_width = img.size[0]
        crop_height = img.size[0]
    elif img.size[0] > img.size[1]:
        crop_width = img.size[1]
        crop_height = img.size[1]
    else:
        img.save(path)
        return None
    img = img.crop(((img_width - crop_width) // 2,
                    (img_height - crop_height) // 2,
                    (img_width + crop_width) // 2,
                    (img_height + crop_height) // 2))
    img.save(path)


def resize_image_formation(im: Image, path: str):
    size = 1200, im.size[1] - 393
    im = im.convert('RGB')
    im.thumbnail(size, Image.Resampling.LANCZOS)
    im = im.crop((0, 0, 1200, 393))
    im = im.convert("L")
    im = im.filter(ImageFilter.GaussianBlur(radius=3))
    target = cv2.imread(path)
    color = np.full(shape=target.shape, fill_value=to_rgb255(colors.to_rgb(random_color(img_estim(im, 127)))), dtype=np.uint8)
    fused_img  = cv2.addWeighted(target, 0.5, color, 0.5, 0)
    cv2.waitKey(0)
    cv2.imwrite(path, fused_img)

def resize_image_picto(im: Image, path: str):
    """Resize l'image pour qu'elle soit carrée et de taille 400x400"""
    size = 512, 512
    im = im.convert('RGB')
    im.thumbnail(size, Image.Resampling.LANCZOS)
    im = im.crop((0, 0, 512, 512))
    im.save(path)


def resize_image_materiel(im: Image, path: str):
    size = 400, im.size[1] - 393
    im = im.convert('RGB')
    im.thumbnail(size, Image.Resampling.LANCZOS)
    im = im.crop((0, 0, 400, 393))
    im.save(path)


def stocker_photo_profile(file):
    try:
        chemin_avatar = "./static/images/photo_profile/" + secure_filename(file.filename)
        file.save(chemin_avatar)
        chemin_avatar = "photo_profile/" + secure_filename(file.filename)
        img = Image.open(file.stream)
    except:
        return "photo_profile/defaut_profile.png"

    resize_image_profile(img, "./static/images/" + chemin_avatar)
    return chemin_avatar


def stocker_picto(file):
    try:
        chemin_picto = "./static/images/icone_fiches/" + secure_filename(file.filename)
        file.save(chemin_picto)
        chemin_picto = secure_filename(file.filename)
        img = Image.open(file.stream)
        resize_image_picto(img, "./static/images/icone_fiches/" + chemin_picto)
        return chemin_picto
    except Exception as e:
        print(e)


def stocker_photo_materiel(file, categorie):
    try:
        chemin_materiel = "./static/images/materiel/"
        if categorie == "Electrique":
            categorie = "elec/"
        elif categorie == "Plomberie":
            categorie = "plomb/"
        elif categorie == "General":
            categorie = "general/"
        
        chemin_materiel = chemin_materiel + categorie + secure_filename(file.filename)
        file.save(chemin_materiel)
        chemin_materiel = categorie + secure_filename(file.filename)
        img = Image.open(file.stream)
        resize_image_materiel(img, "./static/images/materiel/" + chemin_materiel)
        return chemin_materiel
    except:
        return "default_materiel.png"


def stocker_image_formation(file):
    try:
        chemin_image = "./static/images/formation_image/" + secure_filename(file.filename)
        file.save(chemin_image)
        chemin_image = "formation_image/" + secure_filename(file.filename)
        img = Image.open(file.stream)
    except:
        return "formation_image/default_formation.png"

    resize_image_formation(img, "./static/images/" + chemin_image)
    return chemin_image


def process_photo(photo, existing_photo, id_fiche, filename):
    if photo.filename == "" and not existing_photo:
        photo.filename = None
    else:
        save_photo(photo, id_fiche, filename)


def save_photo(photo, id_fiche, filename):
    filename = secure_filename(f"{id_fiche}_{filename}.jpg")
    photo.save(f"./static/images/photo_fiche/{filename}")


def supprimer_photo_profil(file):
    try:
        chemin_avatar = "./static/images/" + file
        os.remove(chemin_avatar)
    except:
        return "erreur suppression photo de profil"
    
def default_image_profil(file):
    try:
        if not os.path.exists('./static/images/' + file):
            chemin_avatar = "./photo_profile/defaut_profile.png"
            db.session.commit()
        else:
            chemin_avatar = file
        return chemin_avatar
    except:
        return "Erreur : pas de photo de profil par défaut"
    
def default_image_formation(file):
    try:
        if not os.path.exists('./static/images/' + file):
            chemin_image = "./formation_image/default_formation.png"
            db.session.commit()
        else:
            chemin_image = file
        return chemin_image
    except:
        return "Erreur : pas d'image de formation par défaut"