from flask import (
    Blueprint,
    Response,
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from custom_paquets.builder import build_materiel
from custom_paquets.converter import changer_date
from custom_paquets.decorateur import educsimple_login_required
from custom_paquets.gestion_filtres_routes import (
    apprenti_existe,
    fiche_by_id_existe,
    fiche_by_numero_existe,
)
from model.apprenti import Apprenti
from model.composer import ComposerPresentation
from model.cours import Cours
from model.ficheintervention import FicheIntervention
from model.laissertrace import LaisserTrace
from model.personnel import Personnel

educ_simple = Blueprint("educ_simple", __name__, url_prefix="/educ-simple")
personnel = Blueprint("personnel", __name__, url_prefix="/educ-simple")

"""
Blueprint pour toutes les routes relatives aux URL des pages des éducateurs simples

Préfixe d'URL : /educ-simple/ .
"""


@educ_simple.route("/", methods=["GET"])
@educsimple_login_required
def redirect_educ_simple():
    """
    Redirige vers la page d'accueil de l'educ simple
    """
    return redirect(url_for("personnel.redirect_personnel"), 302)


@educ_simple.route("/<string:apprenti>/fiches", methods=["GET"])
@educsimple_login_required
def fiches_apprenti(apprenti):
    """
    Page par défaut de l'éducateur simple.
    Ce dernier ne peut que commenter une fiche technique d'un apprenti.

    :return: Les fiches techniques de l'apprenti sélectionné.
    """

    if not Apprenti.get_id_apprenti_by_login(apprenti):
        abort(404)

    apprenti_infos = Apprenti.get_apprenti_by_login(apprenti)
    fiches = FicheIntervention.get_fiches_techniques_finies_par_login(apprenti)
    fiches = changer_date(fiches)
    cours = Cours.get_cours_par_apprenti(Apprenti.get_id_apprenti_by_login(apprenti))
    return render_template("personnel/choix_fiches_apprenti.html", apprenti=apprenti_infos, fiches=fiches, get_nom_cours_by_id=Cours.get_nom_cours_by_id, cours=cours)


@educ_simple.route("/<string:apprenti>/<int:numero>/commentaires", methods=["GET"])
@educsimple_login_required
def visualiser_commentaires(apprenti, numero):
    """
    Page d'affichage des commentaires de la fiche d'identifiant fiche de l'apprenti au login apprenti

    :return: les commentaires de la fiche de l'élève sélectionnée.
    """

    if not Apprenti.get_id_apprenti_by_login(apprenti):
        abort(404)

    if not FicheIntervention.get_id_fiche_apprenti(apprenti, numero):
        abort(404)

    commentaires_educ = LaisserTrace.get_commentaires_type_par_fiche((FicheIntervention.get_id_fiche_apprenti(apprenti, numero)))
    commentaires_appr = LaisserTrace.get_commentaires_type_par_fiche((FicheIntervention.get_id_fiche_apprenti(apprenti, numero)), apprenti="1")
    return render_template("personnel/commentaires.html", apprenti=apprenti, numero=numero, commentaires_educ=commentaires_educ, commentaires_appr=commentaires_appr), 200


@educ_simple.route("/<string:apprenti>/<int:numero>/modifier-commentaires/<string:type_commentaire>", methods=["GET", "POST"])
@educsimple_login_required
def modifier_commentaires(apprenti, numero, type_commentaire):
    """
    Page de modification des commentaires éducateur de la fiche d'identifiant fiche de l'apprenti
    au login apprenti

    :return: la page de modification des commentaires des éducateurs de la fiche de l'élève sélectionnée.
    """

    apprenti_existe(apprenti)
    fiche_by_numero_existe(apprenti, numero)

    if type_commentaire not in ["educateur", "apprenti"]:
        abort(404)
    id_fiche = FicheIntervention.get_id_fiche_apprenti(apprenti, numero)

    id_personnel = Personnel.get_id_personnel_by_login(session.get("name"))

    if type_commentaire == "educateur":
        commentaires = LaisserTrace.get_commentaires_type_par_fiche(id_fiche)
    else:
        commentaires = LaisserTrace.get_commentaires_type_par_fiche(id_fiche, apprenti="1")

    fiche = FicheIntervention.get_fiche_par_id_fiche(id_fiche)
    if request.method == "POST":
        commentaire_texte = request.form["commentaire_texte"]
        eval_texte = request.form["eval_texte"]

        LaisserTrace.modifier_commentaire_texte(fiche.id_fiche, commentaires.horodatage, commentaire_texte, type_commentaire=type_commentaire)

        LaisserTrace.modifier_evaluation_texte(fiche.id_fiche, commentaires.horodatage, eval_texte, type_commentaire=type_commentaire)
        if "Administrateur" in Personnel.get_role_by_login(session.get("name")):
            return redirect(url_for("educ_admin.visualiser_commentaires", apprenti=apprenti, numero=numero), 302)
        else:
            return redirect(url_for("educ_simple.visualiser_commentaires", apprenti=apprenti, numero=numero), 302)

    return Response(
        render_template("personnel/modifier_commentaires.html", apprenti=apprenti, fiche=fiche, commentaires=commentaires, typeCommentaire=type_commentaire, id_personnel=id_personnel), 200
    )


@educ_simple.route("/<string:apprenti>/<int:numero>/ajouter-commentaires/<string:type_commentaire>", methods=["POST", "GET"])
@educsimple_login_required
def ajouter_commentaires(apprenti, numero, type_commentaire):
    """
    Page d'ajout des commentaires éducateur de la fiche d'identifiant fiche de l'apprenti

    :return: la page d'ajout des commentaires des éducateurs de la fiche de l'élève sélectionnée.
    """

    apprenti_existe(apprenti)
    fiche_by_numero_existe(apprenti, numero)
    if type_commentaire not in ["educateur", "apprenti"]:
        abort(404)

    fiche = FicheIntervention.get_fiche_par_id_fiche(FicheIntervention.get_id_fiche_apprenti(apprenti, numero))
    if request.method == "POST":
        if type_commentaire == "apprenti":
            type_c = "1"
        else:
            type_c = "0"
        commentaire_texte = request.form["commentaire"]
        eval_texte = request.form["evaluation"]
        intitule = request.form["intitule"]
        LaisserTrace.ajouter_commentaires_evaluation(fiche.id_fiche, commentaire_texte, eval_texte, None, None, session.get("name"), intitule, type_c)
        return redirect(url_for("educ_simple.visualiser_commentaires", apprenti=apprenti, numero=numero), 302)

    return Response(render_template("personnel/ajouter_commentaires.html", apprenti=apprenti, fiche=fiche, type_commentaire=type_commentaire), 200)


@educ_simple.route("/imprimer-pdf/<int:id_fiche>", methods=["GET"])
@educsimple_login_required
def imprimer_pdf(id_fiche):
    """
    Page d'impression d'une fiche technique par un educ admin

    :return: rendu de la page fiche_pdf.html
    """

    fiche_by_id_existe(id_fiche)

    # verifier que fiche finie
    fiche = FicheIntervention.get_fiche_par_id_fiche(id_fiche)
    FicheIntervention.valider_fiche(fiche.id_fiche)

    materiaux = build_materiel()
    composer_fiche = ComposerPresentation.get_composer_presentation_par_apprenti(fiche.id_fiche)
    return render_template("apprentis/fiche_pdf.html", composition=composer_fiche, fiche=fiche, materiaux=materiaux)
