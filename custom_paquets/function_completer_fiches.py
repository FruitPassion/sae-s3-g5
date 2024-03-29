from flask import request

from model.composer import ComposerPresentation

def complete_form_data(completer_fiche):
    for element in request.form:
        if element == "avancee" or "radio-" in element:
            continue

        if len(request.form.get(f"{element}")) != 0:
            element_data = request.form.get(f"{element}")
        else:
            element_data = None
                
        completer_fiche[f"{element}"] = element_data

def process_material(fiche, ajouter_materiel):
    for element in request.form:
        if "selecteur-" in element and len(request.form.get(f"{element}")) != 0:
            ajouter_materiel[f"{element.replace('selecteur-','')}"] = request.form.get(f"{element}")
        elif "selecteur-" in element:
            ajouter_materiel[f"{element.replace('selecteur-','')}"] = None
    if len(ajouter_materiel) != 0:
        ComposerPresentation.maj_materiaux_fiche(ajouter_materiel, fiche.id_fiche)

def process_radio_input(fiche, completer_fiche):
    for element in request.form:
        if "radio-" in element:
            element = request.form.get(f"{element}")
            completer_fiche[f"{element}"] = "radioed"
    radios = ComposerPresentation.get_radio_radioed(fiche.id_fiche)
    for radio in radios:
        if radio.position_elem not in completer_fiche.keys():
            completer_fiche[f"{radio.position_elem}"] = None

def process_checkboxes(fiche, completer_fiche):
    checkboxes = ComposerPresentation.get_checkbox_on(fiche.id_fiche)
    for checkbox in checkboxes:
        if checkbox.position_elem not in request.form.keys():
            completer_fiche[f"{checkbox.position_elem}"] = None
