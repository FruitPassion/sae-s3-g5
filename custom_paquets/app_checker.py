from pygit2 import Repository

from custom_paquets.gestions_erreur import ConfigurationError, GitBranchError


def check_git_branch(app):
    """
    Vérifie la branche git sur laquelle on se trouve

    :param config: Branch git
    :param app: Application flask
    :return: None
    """
    branche = Repository('.').head.shorthand
    if branche in ["main", "dev"]:
        app.config.from_object(f"config.{branche.capitalize()}Config")
    else:
        raise GitBranchError("Branche inconnue")


def get_current_config():
    """
    Récupère la configuration actuelle de l'application
    :return: Nom de la configuration actuelle
    """
    return Repository('.').head.shorthand