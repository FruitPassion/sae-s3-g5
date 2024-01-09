const btn_desarchiver =
    '<th scope="row" class="align-middle ele-btn-desarchiver" onclick="validation_desarchivage(this)"\n' +
    '                                data-bs-toggle="modal"\n' +
    '                                data-bs-target="#modal-desarchiver">\n' +
    '                                <button><i class="fa fa-archive" aria-hidden="true"></i></button>\n' +
    '                            </th>'

const btn_supprimer =
    '<th scope="row" class="align-middle ele-btn-supprimer" onclick="validation_suppression(this)"\n' +
    '                                data-bs-toggle="modal"\n' +
    '                                data-bs-target="#modal-supprimer">\n' +
    '                                <button><i class="fa fa-trash" aria-hidden="true"></i></button>\n' +
    '                            </th>'


const btn_archiver =
    '<th scope="row" class="align-middle ele-btn-archiver" onclick="validation_archivage(this)"\n' +
    '                                data-bs-toggle="modal"\n' +
    '                                data-bs-target="#modal-archiver">\n' +
    '                                <button><i class="fa fa-archive" aria-hidden="true"></i></button>\n' +
    '                            </th>'

const btn_archiver_apprenti =
    '<th scope="row" class="align-middle ele-btn-archiver-arpprenti"\n' +
    '                                onclick="reinitialiser_formation(this)" data-bs-toggle="modal"\n' +
    '                                data-bs-target="#modal-reinitialiser">\n' +
    '                                <button><i class="fa fa-refresh" aria-hidden="true"></i></button>\n' +
    '                            </th>'

function btn_modifier(route) {
    return '<th scope="row" onclick="passer_parametre_form(this, \'' + route + '\')"\n' +
        '                                class="align-middle ele-btn-modif" data-bs-toggle="modal"\n' +
        '                                data-bs-target="#modal-modifier">\n' +
        '                                <button><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>\n' +
        '                            </th>'
}

function validation_archivage(element) {
    document.getElementById("archiver-value").value = element.parentElement.id.replace('ele-', '');
}

function archiver_apprenti() {
    archiver("apprenti");
}


function archiver_formation() {
    archiver("formation");
}

function archiver_personnel() {
    archiver("personnel");
}

function archiver(route, elementid = "archiver-value") {
    let id_element = document.getElementById(elementid).value;
    let row = document.getElementById("ele-" + id_element);
    let table = document.getElementById("table-archive").getElementsByTagName("tbody")[0];
    let clone = row.cloneNode(true);
    clone.id = "arch-" + clone.id

    afficher_snack("Archivage en cours...", "info");
    $.getJSON("/api/archiver-" + route + "/" + encodeURIComponent(id_element), function (data) {
        if (data["valide"]) {
            afficher_snack("Archivage réussi !", "success");
            if (data["retirer"]) {
                switch (route) {
                    case "personnel":
                    case "apprenti":
                        clone.getElementsByClassName("ele-btn-modif")[0].outerHTML = btn_desarchiver;
                        clone.getElementsByClassName("ele-btn-archiver")[0].outerHTML = btn_supprimer;
                        break;
                    case "formation":
                        clone.getElementsByClassName("ele-btn-modif")[0].outerHTML = btn_desarchiver;
                        clone.getElementsByClassName("ele-btn-archiver")[0].outerHTML = btn_supprimer;
                        clone.getElementsByClassName("ele-btn-archiver-arpprenti")[0].outerHTML = "";
                        break;
                }
                table.appendChild(clone);
                row.parentElement.removeChild(row);
            }
        } else {
            afficher_snack("Archivage échoué.", "error");
        }
    });
}

function validation_desarchivage(element) {
    document.getElementById("desarchiver-value").value = element.parentElement.id.replace('arch-ele-', '');
}

function desarchiver_apprenti() {
    desarchiver("apprenti");
}


function desarchiver_formation() {
    desarchiver("formation");
}


function desarchiver_personnel() {
    desarchiver("personnel");
}

function desarchiver(route) {
    let id_element = document.getElementById("desarchiver-value").value;
    let row = document.getElementById("arch-ele-" + id_element);
    let table = document.getElementById("table-non-archive").getElementsByTagName("tbody")[0];
    let clone = row.cloneNode(true);
    clone.id = clone.id.replace("arch-", "")

    afficher_snack("Desarchivage en cours...", "info");

    $.getJSON("/api/desarchiver-" + route + "/" + encodeURIComponent(id_element), function (data) {
        if (data["valide"]) {
            afficher_snack("Desarchivage réussi !", "success");
            switch (route) {
                case "formation":
                    clone.getElementsByClassName("ele-btn-desarchiver")[0].outerHTML = btn_modifier(route);
                    clone.getElementsByClassName("ele-btn-supprimer")[0].outerHTML = btn_archiver + btn_archiver_apprenti;
                    break;
                case "apprenti":
                case "personnel":
                    clone.getElementsByClassName("ele-btn-desarchiver")[0].outerHTML = btn_modifier(route);
                    clone.getElementsByClassName("ele-btn-supprimer")[0].outerHTML = btn_archiver;
                    break;
            }
            table.appendChild(clone);
            row.parentElement.removeChild(row);
        } else {
            afficher_snack("Desarchivage échoué.", "error");
        }
    });
}