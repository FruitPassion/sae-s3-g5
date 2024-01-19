from PIL import Image, ImageFilter, ImageOps, ImageColor
from werkzeug.utils import secure_filename
from random import randint


def random_color():
    color = []
    for name, code in ImageColor.colormap.items():
        if name not in ["black", "white", "lightgrey", "darkgrey", "grey", "dimgrey", "dimgray", "silver", "gainsboro"]:
            color.append(name)
    return color[randint(0, len(color) - 1)]


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
    im = ImageOps.colorize(im, black=random_color(), white="white")
    im.save(path)


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

