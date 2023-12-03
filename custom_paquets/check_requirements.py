import warnings

import pkg_resources
import sys
import subprocess

def checking():
    """
    Permet de verifier si tous les prerequis sont installés et à la bonne version.
    En cas d'echec, installe et mets à jour dans les bonnes versions.
    """
    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        dependencies = [s.strip() for s in lines]

    try:
        pkg_resources.require(dependencies)
    except Exception as e:
        print("Mise à jour des prérequis : " + str(e))
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'])


