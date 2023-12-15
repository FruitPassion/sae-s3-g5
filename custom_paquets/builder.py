from model.composer import get_composer_categorie, get_composer_non_categorie, get_elements_base
from model.pictogramme import get_pictogramme, get_all_pictogrammes


def build_categories(id_fiche):
    composer_cat = get_composer_categorie(id_fiche)
    composer_non_cat = get_composer_non_categorie(id_fiche)
    pictogrammes = get_pictogramme(id_fiche)
    bases = get_elements_base()
    for i in range(len(composer_cat)):
        composer_cat[i] = composer_cat[i] | get_common_element(composer_cat[i], bases)
        composer_cat[i]["elements"] = []
        for elements_non_cat in composer_non_cat:
            if composer_cat[i]["position_elem"][0] == elements_non_cat["position_elem"][0]:
                elements_non_cat = elements_non_cat | get_common_element(elements_non_cat, bases)
                composer_cat[i]["elements"].append(elements_non_cat)
            for pict in pictogrammes:
                if pict["id_pictogramme"] == elements_non_cat["pictogramme"]:
                    elements_non_cat["pictogramme"] = pict["url"]
    return composer_cat


def build_pictogrammes():
    pictos = get_all_pictogrammes()
    to_return = {}
    for dico in pictos:
        to_return[dico["categorie"]] = {}
    for key in to_return:
        for dico in pictos:
            if dico["categorie"] == key and dico["categorie"] != "Autre":
                to_return[key][dico["souscategorie"]] = []
            to_return["Autre"]["Autre"] = []
        for element in to_return[key].keys():
            for dico in pictos:
                _ = {"url": dico["url"], "label": dico["label"], "id": dico["id_pictogramme"]}
                if dico["souscategorie"] == element and dico["categorie"] != "Autre":
                    to_return[key][dico["souscategorie"]].append(_)
                elif dico["categorie"] == "Autre" and _ not in to_return["Autre"]["Autre"]:
                    to_return["Autre"]["Autre"].append(_)

    return to_return


def get_common_element(element, bases):
    for base in bases:
        if element["id_element"] == base["id_element"]:
            return base
    return {}
