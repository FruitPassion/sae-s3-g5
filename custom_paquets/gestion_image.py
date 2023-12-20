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


def stocker_photo_profile(file):
    if file:
        chemin_avatar = "./static/images/photo_profile/" + secure_filename(file.filename)
        file.save(chemin_avatar)
        chemin_avatar = "photo_profile/" + secure_filename(file.filename)
    else:
        chemin_avatar = "photo_profile/" + "default_profile.png"
    img = Image.open(file.stream)
    resize_image_profile(img, "./static/images/" + chemin_avatar)
    return chemin_avatar


def stocker_image_formation(file):
    if file:
        chemin_image = "./static/images/formation_image/" + secure_filename(file.filename)
        file.save(chemin_image)
        chemin_image = "formation_image/" + secure_filename(file.filename)
    else:
        chemin_image = "formation_image/" + "default_formation.png"
    img = Image.open(file.stream)
    resize_image_formation(img, "./static/images/" + chemin_image)
    return chemin_image
