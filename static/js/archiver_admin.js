function validation_archivage(element){
    document.getElementById("archiver-value").value = element.parentElement.id.replace('ele-','');
}

function archiver_apprenti(){
    archiver("apprenti");
}


function archiver_formation(){
    archiver("formation");
}


function archiver_personnel(){
    archiver("personnel");
}

function archiver(route){
    let id_formation = document.getElementById("archiver-value").value;
    let row = document.getElementById("ele-" + id_formation);

    afficher_snack("Archivage en cours...", "info");

    $.getJSON("/api/archiver-"+route+"/" + encodeURIComponent(id_formation), function (data) {
        if (data["valide"]) {
            afficher_snack("Archivage réussi !", "success");
            row.parentElement.removeChild(row);
            document.getElementById("recharger-2").removeAttribute("hidden");
        } else {
            afficher_snack("Archivage échoué.", "error");
        }
    });
}

function validation_desarchivage(element){
    document.getElementById("desarchiver-value").value = element.parentElement.id.replace('arch-ele-','');
}

function desarchiver_apprenti(){
    desarchiver("apprenti");
}


function desarchiver_formation(){
    desarchiver("formation");
}


function desarchiver_personnel(){
    desarchiver("personnel");
}

function desarchiver(route){
    let id_formation = document.getElementById("desarchiver-value").value;
    let row = document.getElementById("arch-ele-" + id_formation);

    afficher_snack("Desarchivage en cours...", "info");

    $.getJSON("/api/desarchiver-"+route+"/" + encodeURIComponent(id_formation), function (data) {
        if (data["valide"]) {
            afficher_snack("Desarchivage réussi !", "success");
            row.parentElement.removeChild(row);
            document.getElementById("recharger-1").removeAttribute("hidden");
        } else {
            afficher_snack("Desarchivage échoué.", "error");
        }
    });
}