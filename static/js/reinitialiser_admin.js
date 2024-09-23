function validation_reinitialisation_formation(element) {
    document.getElementById("reinitialiser-value").value = element.parentElement.id.replace('ele-', '');
}


function reinitialiser() {
    let id_element = document.getElementById("reinitialiser-value").value;

    afficher_snack("Réinitialisation en cours...", "info");

    const requestOptions = {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' ,
        'X-CSRFToken': csrf_token },
    };

    fetch(baseApiUrl + "/api/reinitialiser-formation/" + encodeURIComponent(id_element), requestOptions)
        .then(response => response.json()) // Convertir la réponse en JSON
        .then(data => {
            if (data["valide"]) {
                afficher_snack("Réinitialisation réussie !", "success");
                $("#modal-lien").modal("toggle");
            } else {
                afficher_snack("Réinitialisation échouée.", "error");
            }
    });
}