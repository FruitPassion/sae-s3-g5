function validation_reinitialisation_formation(element) {
    document.getElementById("reinitialiser-value").value = element.parentElement.id.replace('ele-', '');
}


function reinitialiser() {
    let id_element = document.getElementById("reinitialiser-value").value;

    afficher_snack("Réinitialisation en cours...", "info");

    $.getJSON("/api/reinitialiser-formation/" + encodeURIComponent(id_element), function (data) {
        if (data["valide"]) {
            afficher_snack("Réinitialisation réussie !", "success");
            $("#modal-lien").modal("toggle");
        } else {
            afficher_snack("Réinitialisation échouée.", "error");
        }
    });
}