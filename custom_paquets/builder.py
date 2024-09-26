from model.composer import ComposerPresentation
from model.materiel import Materiel
from model.pictogramme import Pictogramme


def build_categories(id_fiche):
    composer_cat = ComposerPresentation.get_composer_categorie(id_fiche)
    composer_non_cat = ComposerPresentation.get_composer_non_categorie(id_fiche)

    pictogrammes = Pictogramme.get_pictogrammes(id_fiche)
    bases = ComposerPresentation.get_elements_base()
    for i in range(len(composer_cat)):
        composer_cat[i] = composer_cat[i] | get_common_element(composer_cat[i], bases)
        composer_cat[i]["elements"] = []
        for elements_non_cat in composer_non_cat:
            if composer_cat[i]["position_elem"][0] == elements_non_cat["position_elem"][0]:
                elements_non_cat = elements_non_cat | get_common_element(elements_non_cat, bases)
                composer_cat[i]["elements"].append(elements_non_cat)
            for pict in pictogrammes:
                if pict.id_pictogramme == elements_non_cat["pictogramme"]:
                    elements_non_cat["pictogramme"] = pict.url
    return composer_cat


def check_ressenti(build):
    nb = 0
    for e in build[5]["elements"]:
        if e["text"] is None:
            nb += 1
    return nb != 5


def build_materiel():
    materiaux = Materiel.get_all_materiel()
    to_return = []
    for materiel in materiaux:
        # check if categorie already in one of to_return dictionnaries at key "nom"
        if materiel.categorie not in [categorie["nom"] for categorie in to_return]:
            to_return.append({"nom": f"{materiel.categorie}", "elements": []})

    for categorie in to_return:
        for materiel in materiaux:
            if materiel.categorie == categorie["nom"]:
                categorie["elements"].append({"nom": materiel.nom, "id_materiel": materiel.id_materiel, "lien": materiel.lien})
    return to_return


def build_pictogrammes():
    pictogrammes = Pictogramme.get_all_pictogrammes()
    to_return = {}
    for picto in pictogrammes:
        to_return[picto.categorie] = {}
    for key in to_return:
        for picto in pictogrammes:
            if picto.categorie == key and picto.categorie != "Autre":
                to_return[key][picto.souscategorie] = []
            to_return["Autre"]["Autre"] = []
        build_elements(key, to_return, pictogrammes)
    return to_return


def build_elements(key, to_return, pictogrammes):
    for element in to_return[key].keys():
        for picto in pictogrammes:
            _ = {"url": picto.url, "label": picto.label, "id": picto.id_pictogramme}
            if picto.souscategorie == element and picto.categorie != "Autre":
                to_return[key][picto.souscategorie].append(_)
            elif picto.categorie == "Autre" and _ not in to_return["Autre"]["Autre"]:
                to_return["Autre"]["Autre"].append(_)


def get_common_element(element, bases):
    for base in bases:
        if element["id_element"] == base["id_element"]:
            return base
    return {}
