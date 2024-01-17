import xlsxwriter
from custom_paquets.converter import changer_date

from model.apprenti import get_apprentis_for_xls
from model.ficheintervention import get_fiches_techniques_par_login
from model.trace import get_commentaires_par_fiche


def generer_xls_apprentis(id_formation):
    workbook = xlsxwriter.Workbook("./static/files/apprentis.xlsx")
    cell_header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 
                                              'border': 1, 'text_wrap': True})
    cell_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
   
    apprentis = get_apprentis_for_xls(id_formation)

    col1 = "Nom"
    col2 = "Prénom"
    col3 = "Login"
    col4 = "Adaptation en situation d'examen"
    col5 = "Nombre fiches abandonnées"
    col6 = "Nombre fiches en cours"
    col7 = "Nombre fiches terminées"
    col8 = "Nombre total fiches"

    for i in range(len(apprentis)):

        worksheet = workbook.add_worksheet(apprentis[i].prenom + ' ' + apprentis[i].nom)
        
        fiches = get_fiches_techniques_par_login(apprentis[i].login)
        fiches = changer_date(fiches)

        nb_fiches_abandonnees, nb_fiches_en_cours, nb_fiches_finies = 0, 0, 0
        for j in range(len(fiches)):
            if fiches[j].etat_fiche == 0:
                nb_fiches_en_cours += 1
            elif fiches[j].etat_fiche == 1:
                nb_fiches_finies += 1

                commentaires = get_commentaires_par_fiche(fiches[j].id_fiche)

                for k in range(len(commentaires)):
                    worksheet.write(f'F{k * 2 + 4}',
                                    f"Commentaire de la fiche {commentaires[k].id_fiche} du {fiches[j].date_creation}", cell_format)
                    worksheet.write(f'G{k * 2 + 4}', commentaires[k].commentaire_texte, cell_format)
                    worksheet.write(f'F{k * 2 + 4}', None)

            elif fiches[j].etat_fiche == 2:
                nb_fiches_abandonnees += 1

        worksheet.write('A1', col1, cell_header_format)
        worksheet.write('B1', col2, cell_header_format)
        worksheet.write('C1', col3, cell_header_format)
        worksheet.write('D1', col4, cell_header_format)
        worksheet.write('F1', col5, cell_header_format)
        worksheet.write('G1', col6, cell_header_format)
        worksheet.write('H1', col7, cell_header_format)
        worksheet.write('I1', col8, cell_header_format)

        worksheet.write('A2', apprentis[i].nom, cell_format)
        worksheet.write('B2', apprentis[i].prenom, cell_format)
        worksheet.write('C2', apprentis[i].login, cell_format)
        worksheet.write('D2', apprentis[i].adaptation_situation_examen, cell_format)
        worksheet.write('F2', nb_fiches_abandonnees, cell_format)
        worksheet.write('G2', nb_fiches_en_cours, cell_format)
        worksheet.write('H2', nb_fiches_finies, cell_format)
        worksheet.write('I2', len(fiches), cell_format)

        worksheet.autofit()

    workbook.close()
