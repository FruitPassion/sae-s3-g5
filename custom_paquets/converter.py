from unidecode import unidecode


def convert_to_dict(elements):
    element_list = []
    if str(type(elements)) == "<class 'sqlalchemy.engine.row.Row'>":
        element_list = elements.__dict__
    else:
        try:
            for element in elements:
                element_list.append(element.__dict__)
        except:
            for element in elements:
                element_list.append(element._asdict())
    return element_list


def generate_login(nom, prenom):
    login = unidecode(prenom[0:2].upper().strip()) + unidecode(nom[0].upper().strip()) + str(
        len(nom.strip() + prenom.strip())).zfill(2)
    return login


def changer_date(fiches):
    for fiche in fiches:
        fiche.date_convertis = fiche.date_creation.strftime("%d/%m/%Y")
    return fiches
