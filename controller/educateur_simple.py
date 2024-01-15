from flask import Blueprint, render_template, request, session, redirect, url_for

from custom_paquets.converter import changer_date
from custom_paquets.decorateur import educsimple_login_required
from custom_paquets.gestion_audio import stocker_audio_commentaire
from model.apprenti import get_apprenti_by_login, get_id_apprenti_by_login
from model.ficheintervention import get_fiches_techniques_finies_par_login, get_fiche_par_id_apprenti, get_nom_cours_by_id
from model.trace import get_commentaires_par_fiche, modifier_commentaire_texte, modifier_evaluation_texte, \
    get_commentaires_educ_par_fiche, ajouter_commentaires_evaluation, modifier_commentaire_audio, \
    modifier_eval_audio, get_audio_commentaire
    
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
    
    :return: les fiches techniques de l'apprenti sélectionné.
    """

    apprenti_infos = get_apprenti_by_login(apprenti)
    fiches = get_fiches_techniques_finies_par_login(apprenti)
    fiches = changer_date(fiches)
    return render_template("personnel/choix_fiches_apprenti.html", apprenti=apprenti_infos, fiches=fiches, get_nom_cours_by_id=get_nom_cours_by_id)


@educ_simple.route("/<apprenti>/<fiche>/commentaires", methods=["GET"])
@educsimple_login_required
def visualiser_commentaires(apprenti, fiche):
    """
    Page d'affichage des commentaires de la fiche d'identifiant fiche de l'apprenti au login apprenti
    
    :return: les commentaires de la fiche de l'élève sélectionnée.
    """

    commentaires = get_commentaires_par_fiche(fiche)
    return render_template("personnel/commentaires.html", apprenti=apprenti, fiche=fiche,
                           commentaires=commentaires), 200


@educ_simple.route("/<apprenti>/<fiche>/modifier-commentaires", methods=["GET", "POST"])
@educsimple_login_required
def modifier_commentaires(apprenti, fiche):
    """
    Page de modification des commentaires éducateur de la fiche d'identifiant fiche de l'apprenti 
    au login apprenti
    
    :return: la page de modification des commentaires des éducateurs de la fiche de l'élève sélectionnée.
    """

    commentaires = get_commentaires_educ_par_fiche(fiche)
    fiche = get_fiche_par_id_apprenti(get_id_apprenti_by_login(apprenti))
    if request.method == 'POST':
        commentaire_texte = request.form["commentaire_texte"]
        eval_texte = request.form["eval_texte"]
        commentaire_audio = request.form.get("commentaire_audio")
        print(request.form)
        if commentaire_audio in request.files and len(request.files.get("commentaire_audio").filename) != 0: 
            f = request.files.get("commentaire_audio")
            chemin_audio = stocker_audio_commentaire(f)
            if chemin_audio:
                modifier_commentaire_audio(fiche["id_fiche"], commentaires["horodatage"], chemin_audio)                        
        else:
            chemin_audio = get_audio_commentaire(commentaire_audio)
        modifier_commentaire_texte(fiche["id_fiche"], commentaires["horodatage"], commentaire_texte)
        modifier_evaluation_texte(fiche["id_fiche"], commentaires["horodatage"], eval_texte)
        
        return redirect(url_for('educ_simple.visualiser_commentaires', apprenti=apprenti, fiche=fiche["id_fiche"]), 200)
    return render_template("personnel/modifier_commentaires.html", apprenti=apprenti, fiche=fiche,
                           commentaires=commentaires), 200


@educ_simple.route("/<apprenti>/<fiche>/ajouter-commentaires", methods=["POST", "GET"])
@educsimple_login_required
def ajouter_commentaires(apprenti, fiche):
    """
    Page d'ajout des commentaires éducateur de la fiche d'identifiant fiche de l'apprenti
    
    :return: la page d'ajout des commentaires des éducateurs de la fiche de l'élève sélectionnée.
    """
    id_apprenti = get_id_apprenti_by_login(apprenti)
    fiche = get_fiche_par_id_apprenti(id_apprenti)
    if request.method == 'POST':
        commentaire_texte = request.form["commentaire"]
        eval_texte = request.form["evaluation"]
        intitule = request.form["intitule"]
        ajouter_commentaires_evaluation(fiche["id_fiche"], commentaire_texte, eval_texte, None, None, session.get("name"), intitule)
        return redirect(url_for('educ_simple.visualiser_commentaires', apprenti=apprenti, fiche=fiche["id_fiche"]), 200)
    return render_template("personnel/ajouter_commentaires.html", apprenti=apprenti, fiche=fiche), 200

