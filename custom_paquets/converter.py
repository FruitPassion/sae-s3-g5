from unidecode import unidecode
import xlsxwriter
from model.apprenti import get_apprentis_by_formation
from model.ficheintervention import get_fiche_par_id_apprenti
from model.apprenti import get_apprentis_by_formation


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


def generer_xls_apprentis(id_formation):
    """
    Exporte une formation en fichier au format xls

    """
    workbook = xlsxwriter.Workbook('Apprentis.xlsx')
    apprentis = get_apprentis_by_formation(id_formation)
    for i in range(1, len(apprentis) + 1):
        worksheet = workbook.add_worksheet("Apprenti" + i)
        for id_apprenti, nom, prenom, login, mdp, photo, essais, archive, adaptation_situation_examen in apprentis:
            nb_fiches = len(get_fiche_par_id_apprenti(id_apprenti))

            worksheet.write('A1', 'Id_apprenti')
            worksheet.write('B1', 'Nom')
            worksheet.write('C1', 'Prenom')
            worksheet.write('D1', 'Login')
            worksheet.write('E1', 'Mdp')
            worksheet.write('F1', 'Photo')
            worksheet.write('G1', 'Essais')
            worksheet.write('H1', 'Archive')
            worksheet.write('I1', 'Adaptation')
            worksheet.write('J1', 'Nb de fiches associées')
            worksheet.write('A2', id_apprenti)
            worksheet.write('B2', nom)
            worksheet.write('C2', prenom)
            worksheet.write('D2', login)
            worksheet.write('E2', mdp)
            worksheet.write('F2', photo)
            worksheet.write('G2', essais)
            worksheet.write('H2', archive)
            worksheet.write('I2', adaptation_situation_examen)
            worksheet.write('J2', nb_fiches)

    workbook.close()