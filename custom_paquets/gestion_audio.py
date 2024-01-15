from werkzeug.utils import secure_filename


def stocker_audio_commentaire(file):
    try:
        chemin_audio = "./static/audio/" + secure_filename(file.filename)
        file.save(chemin_audio)
        chemin_audio = "audio/" + secure_filename(file.filename)
    except:
        return None

    return chemin_audio
