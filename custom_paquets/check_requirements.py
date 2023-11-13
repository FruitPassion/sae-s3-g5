import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
import sys
import subprocess


def checking():
    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        dependencies = [s.strip() for s in lines]

    try:
        pkg_resources.require(dependencies)
    except:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'])
