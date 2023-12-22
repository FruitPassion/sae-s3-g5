from pygit2 import Repository

from custom_paquets.gestions_erreur import ConfigurationError, LogOpeningError, GitBranchError


def check_config(config):
    """
    Vérifie la configuration demandée
    :param config: Nom de la configuration demandée
    :return: True si la configuration est valide
    """
    if config not in [None, "Developpement"]:
        raise ConfigurationError("Configuration invalide")
    return True


def check_git_branch(config, app):
    """
    Vérifie la branche git sur laquelle on se trouve

    :param config: Branch git
    :param app: Application flask
    :return: None
    """
    if Repository('.').head.shorthand == "dev" or config == "Developpement":
        # Effacer fichier de logs
        if open('app.log', 'w').close():
            raise LogOpeningError("Impossible d'ouvrir le fichier de log")
        app.config.from_object('config.DevConfig')
    elif Repository('.').head.shorthand == "main":
        app.config.from_object('config.ProdConfig')
    else:
        raise GitBranchError("Branche inconnue")