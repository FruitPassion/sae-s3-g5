import sys

from custom_paquets.gestions_erreur import ConfigurationError


def check_config(config):
    """
    Vérifie la configuration demandée
    :param config: Nom de la configuration demandée
    :return: True si la configuration est valide
    """
    if config not in ["dev", "prod", "test"]:
        raise ConfigurationError("Argument de lancement incorrect (dev, test ou prod)")
    return True


def lire_config(nom_fichier):
    try:
        with open(nom_fichier, "r") as fichier:
            contenu = fichier.read()
            return contenu
    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} n'a pas été trouvé.")
        sys.exit(1)
