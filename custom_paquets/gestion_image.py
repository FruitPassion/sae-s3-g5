from PIL import Image


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
