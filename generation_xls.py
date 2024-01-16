import xlsxwriter
from custom_paquets.converter import changer_date

from model.apprenti import get_apprentis_for_xls
from model.ficheintervention import get_fiches_techniques_par_login
from model.trace import get_commentaires_par_fiche


def generer_xls_apprentis(id_formation):
    workbook = xlsxwriter.Workbook('static/files/apprentis.xlsx')
    cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
    apprentis = get_apprentis_for_xls(id_formation)

    col1 = "Nom"
    col2 = "Prénom"
    col3 = "Login"
    col4 = "Adaptation en situation d'examen"
    col5 = "Nombre fiches abadonnées"
    col6 = "Nombre fiches en cours"
    col7 = "Nombre fiches terminées"
    col8 = "Nombre total fiches"

    for i in range(len(apprentis)):

        worksheet = workbook.add_worksheet(f'Apprenti {i + 1}')

        fiches = get_fiches_techniques_par_login(apprentis[i]["login"])
        fiches = changer_date(fiches)

        nb_fiches_abandonnees, nb_fiches_en_cours, nb_fiches_finies = 0, 0, 0
        for j in range(len(fiches)):
            if fiches[j].etat_fiche == 0:
                nb_fiches_en_cours += 1
            elif fiches[j].etat_fiche == 1:
                nb_fiches_finies += 1

                commentaires = get_commentaires_par_fiche(fiches[j].id_fiche)

                for k in range(len(commentaires)):
                    worksheet.write(f'F{k * 3 + 4}',
                                    f"Commentaire de la fiche {commentaires[k].id_fiche} du {fiches[j].date_creation}")
                    worksheet.write(f'F{k * 3 + 5}', commentaires[k].commentaire_texte)
                    worksheet.write(f'F{k * 3 + 6}', None)

            elif fiches[j]['etat_fiche'] == 2:
                nb_fiches_abandonnees += 1

        worksheet.write('A1', col1, cell_format)
        worksheet.write('B1', col2, cell_format)
        worksheet.write('C1', col3, cell_format)
        worksheet.write('D1', col4, cell_format)
        worksheet.write('F1', col5, cell_format)
        worksheet.write('G1', col6, cell_format)
        worksheet.write('H1', col7, cell_format)
        worksheet.write('I1', col8, cell_format)

        worksheet.write('A2', apprentis[i]["nom"])
        worksheet.write('B2', apprentis[i]["prenom"])
        worksheet.write('C2', apprentis[i]["login"])
        worksheet.write('D2', apprentis[i]["adaptation_situation_examen"])
        worksheet.write('F2', nb_fiches_abandonnees)
        worksheet.write('G2', nb_fiches_en_cours)
        worksheet.write('H2', nb_fiches_finies)
        worksheet.write('I2', len(fiches))

    workbook.close()
