function validation_suppression(element){
    document.getElementById("supprimer-value").value = element.parentElement.id.replace('arch-ele-','');
}

function supprimer_apprenti(){
    supprimer("apprenti");
}


function supprimer_formation(){
    supprimer("formation");
}


function supprimer_personnel(){
    supprimer("personnel");
}


function supprimer_materiel(){
    supprimer("materiel");
}


function supprimer(route){
    let id_element = document.getElementById("supprimer-value").value;
    let row = document.getElementById("arch-ele-" + id_element);

    afficher_snack("Suppression en cours...", "info");

    $.getJSON("/api/supprimer-"+route+"/" + encodeURIComponent(id_element), function (data) {
        if (data["valide"]) {
            afficher_snack("Suppression réussie !", "success");
            row.parentElement.removeChild(row);
        } else {
            afficher_snack("Suppression échouée.", "error");
        }
    });
}
