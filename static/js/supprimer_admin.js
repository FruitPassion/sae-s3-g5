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


function supprimer_cours(){
    supprimer("cours");
}


function supprimer(route){
    let id_element = document.getElementById("supprimer-value").value;
    let row = document.getElementById("arch-ele-" + id_element);

    afficher_snack("Suppression en cours...", "info");

    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' ,
        'X-CSRFToken': csrf_token },
    };

    fetch(baseApiUrl + "/api/"+route+"/" + encodeURIComponent(id_element), requestOptions)
        .then(response => response.json()) // Convertir la réponse en JSON
        .then(data => {
            if (data["valide"]) {
                afficher_snack("Suppression réussie !", "success");
                row.parentElement.removeChild(row);
            } else {
                afficher_snack("Suppression échouée.", "error");
            }
        });
}
