from flask import Blueprint, render_template

from custom_paquets.decorateur import educsimple_login_required
from model.apprenti import get_apprenti_by_login
from model.ficheintervention import get_fiches_techniques_finies_par_login
from model.trace import get_commentaires_par_fiche

educ_simple = Blueprint("educ_simple", __name__, url_prefix="/educ-simple")


'''
Blueprint pour toutes les routes relatives aux URL des pages des éducateurs simples

Préfixe d'URL : /educ-simple/ .
'''


@educ_simple.route("/<apprenti>/fiches", methods=["GET"])
@educsimple_login_required
def fiches_apprenti(apprenti):
    """
    Page par défaut de l'éducateur simple.
    Ce dernier ne peut que commenter une fiche technique d'un apprenti.
    
    :return: les fiches techniques de l'élève sélectionné.
    """

    apprenti_infos = get_apprenti_by_login(apprenti)
    fiches = get_fiches_techniques_finies_par_login(apprenti)
    return render_template("personnel/choix_fiches_apprenti.html", apprenti=apprenti_infos[0], fiches=fiches)


@educ_simple.route("/<apprenti>/<fiche>/commentaires", methods=["GET"])
@educsimple_login_required
def visualiser_commentaires(apprenti, fiche):
    """
    Page d'affichage des commentaires de la fiche d'identifiant fiche de l'apprenti au login apprenti
    
    :return: les commentaires de la fiche de l'élève sélectionnée.
    """

    commentaires = get_commentaires_par_fiche(fiche)
    return render_template("personnel/commentaires.html", apprenti = apprenti, fiche=fiche, commentaires = commentaires), 200


@educ_simple.route("/<apprenti>/<fiche>/modifier-commentaires/<commentaire_texte>/<eval_texte>", methods=["GET"])
@educsimple_login_required
def modifier_commentaires(apprenti, fiche, commentaire_texte, eval_texte):
    """
    Page de modification des commentaires éducateur de la fiche d'identifiant fiche de l'apprenti 
    au login apprenti
    
    :return: la page de modification des commentaires des éducateurs de la fiche de l'élève sélectionnée.
    """

    commentaires = get_commentaires_par_fiche(fiche)
    return render_template("personnel/modifier_commentaires.html", apprenti = apprenti, fiche=fiche, commentaire_texte = commentaire_texte, eval_texte = eval_texte), 200
