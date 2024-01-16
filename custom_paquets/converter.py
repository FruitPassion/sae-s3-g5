from unidecode import unidecode


def convert_to_dict(classes):
    classes_list = []
    if str(type(classes)) == "<class 'sqlalchemy.engine.row.Row'>":
        classes_list = classes._asdict()
    else:
        for classe in classes:
            classes_list.append(classe._asdict())
    return classes_list


def generate_login(nom, prenom):
    login = unidecode(prenom[0:2].upper().strip()) + unidecode(nom[0].upper().strip()) + str(
        len(nom.strip() + prenom.strip())).zfill(2)
    return login


def changer_date(fiches):
    for fiche in fiches:
        fiche.date_creation = fiche.date_creation.strftime("%d/%m/%Y")
    return fiches
