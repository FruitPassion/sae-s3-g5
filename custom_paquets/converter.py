from unidecode import unidecode


def convert_to_dict(posts):
    post_list = []
    if str(type(posts)) == "<class 'sqlalchemy.engine.row.Row'>":
        post_list = posts._asdict()
    else:
        for post in posts:
            post_list.append(post._asdict())
    return post_list


def generate_login(nom, prenom):
    login = unidecode(prenom[0:2].upper().strip()) + unidecode(nom[0].upper().strip()) + str(
        len(nom.strip() + prenom.strip())).zfill(2)
    return login


def changer_date(fiches):
    for fiche in fiches:
        fiche["date_creation"] = fiche["date_creation"].strftime("%d/%m/%Y")
    return fiches
