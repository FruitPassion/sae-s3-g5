import logging


def logging_erreur(e, message='Exception occurred : '):
    f = open("app.log", "r")
    ligne_depart = len(f.readlines())+1
    logging.exception(message+str(e))
    ligne_fin = ligne_depart+(len(f.readlines())-1)
    f.close()
    f = open("app.log", "r")
    mess = ''
    for i, line in enumerate(f):
        if "^^^^^" in line.strip():
            continue
        if ligne_depart <= i <= ligne_fin:
            mess = mess + line.strip() + '<br>'
    f.close()


class ProjectError(Exception):
    pass


class GitBranchError(ProjectError):
    pass


class ConfigurationError(ProjectError):
    pass

