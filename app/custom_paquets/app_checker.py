from custom_paquets.gestions_erreur import ConfigurationError


def check_config(config):
    """
    Vérifie la configuration demandée
    :param config: Nom de la configuration demandée
    :return: True si la configuration est valide
    """
    if config not in ["dev", "prod", "test"]:
        raise ConfigurationError("La configuration demandée n'est pas valide.")
    return True
