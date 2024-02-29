from flask import abort, session
from model.apprenti import Apprenti
from model.ficheintervention import FicheIntervention
from model.formation import Formation


def fiche_by_numero_existe(apprenti, numero):
    if not FicheIntervention.get_id_fiche_apprenti(apprenti, numero):
        abort(404)

def fiche_by_id_existe(fiche):
    if not FicheIntervention.get_fiche_par_id_fiche(fiche):
        abort(404)

def formation_existe(nom):
    if not Formation.get_formation_id_par_nom_formation(nom):
        abort(404)

def apprenti_existe(login):
    if not Apprenti.get_id_apprenti_by_login(login):
        abort(404)