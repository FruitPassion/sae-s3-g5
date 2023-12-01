from model.composer import get_composer_categorie, get_composer_non_categorie, get_elements_base


def build_categories(id_fiche):
    composer_cat = get_composer_categorie(id_fiche)
    composer_non_cat = get_composer_non_categorie(id_fiche)
    bases = get_elements_base()
    for i in range(len(composer_cat)):
        composer_cat[i] = composer_cat[i] | get_common_element(composer_cat[i], bases)
        composer_cat[i]["elements"] = []
        for elements_non_cat in composer_non_cat:
            if composer_cat[i]["position_elem"][0] == elements_non_cat["position_elem"][0]:
                elements_non_cat = elements_non_cat | get_common_element(elements_non_cat, bases)
                composer_cat[i]["elements"].append(elements_non_cat)
    return composer_cat


def get_common_element(element, bases):
    for base in bases:
        if element["id_element"] == base["id_element"]:
            return base
    return {}

