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


def check_accessibilite_fiche(id_fiche, accessible):
    # Vérifie l'accessibilité de la fiche id_fiche en fonction de son état
    # 0 : en cours, 1 : terminée, 2 : arrêtée
    if accessible == 0:
        # Si la fiche est en cours, alors elle doit être accessible (modifiable par educ admin ou remplissable par apprenti)
        if not FicheIntervention.get_etat_fiche_par_id_fiche(id_fiche) == 0:
            abort(404)
    else:
        # Sinon, elle ne doit pas être accessible
        if FicheIntervention.get_etat_fiche_par_id_fiche(id_fiche) == 0:
            abort(404)
