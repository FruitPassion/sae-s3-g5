import warnings

import pkg_resources
import sys
import subprocess


def checking():
    """
    Permet de vérifier si tous les prérequis sont installés et à la bonne version.
    En cas d'échec, les installe et les met à jour dans les bonnes versions.
    """
    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        dependencies = [s.strip() for s in lines]

    try:
        pkg_resources.require(dependencies)
    except Exception as e:
        print("Mise à jour des prérequis : " + str(e))
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'])


