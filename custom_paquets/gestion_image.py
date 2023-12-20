from PIL import Image
from werkzeug.utils import secure_filename


def resize_image(img: Image, path: str):
    img_width, img_height = img.size
    if img.size[0] < img.size[1]:
        crop_width = img.size[0]
        crop_height = img.size[0]
    elif img.size[0] > img.size[1]:
        crop_width = img.size[1]
        crop_height = img.size[1]
    else:
        img.save(path)
    img = img.crop(((img_width - crop_width) // 2,
                    (img_height - crop_height) // 2,
                    (img_width + crop_width) // 2,
                    (img_height + crop_height) // 2))
    img.save(path)

def stocker_photo_profile(file):
    if file:
        chemin_avatar = "./static/images/photo_profile/" + secure_filename(file.filename)
        file.save(chemin_avatar)
        chemin_avatar = "photo_profile/" + secure_filename(file.filename)
    else:
        chemin_avatar = "photo_profile/" + "default_profile.png"
    img = Image.open(file.stream)
    resize_image(img, "./static/images/" + chemin_avatar)
    return chemin_avatar

def stocker_image_formation(file):
    if file:
        chemin_image = "./static/images/formation_image/" + secure_filename(file.filename)
        file.save(chemin_image)
        chemin_image = "formation_image/" + secure_filename(file.filename)
    else:
        chemin_image = "formation_image/" + "default_formation.png"
    img = Image.open(file.stream)
    resize_image(img, "./static/images/" + chemin_image)
    return chemin_image