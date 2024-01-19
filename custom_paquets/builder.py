from model.composer import get_composer_categorie, get_composer_non_categorie, get_elements_base
from model.materiel import get_all_materiel
from model.pictogramme import get_pictogrammes, get_all_pictogrammes


def build_categories(id_fiche):
    composer_cat = get_composer_categorie(id_fiche)
    composer_non_cat = get_composer_non_categorie(id_fiche)

    pictogrammes = get_pictogrammes(id_fiche)
    bases = get_elements_base()
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


def build_materiel():
    materiaux = get_all_materiel()
    to_return = []
    for materiel in materiaux:
        # check if categorie already in one of to_return dictionnaries at key "nom"
        if materiel.categorie not in [categorie["nom"] for categorie in to_return]:
            to_return.append({"nom": f"{materiel.categorie}", "elements": []})

    for categorie in to_return:
        for materiel in materiaux:
            if materiel.categorie == categorie["nom"]:
                categorie["elements"].append({"nom": materiel.nom, "id_materiel": materiel.id_materiel,
                                              "lien": materiel.lien})
    return to_return


def build_pictogrammes():
    pictogrammes = get_all_pictogrammes()
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
