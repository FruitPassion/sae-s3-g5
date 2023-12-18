let visible = true;

function visibilite() {
    if (visible) {
        document.getElementById('password').setAttribute("type", "text");
        document.getElementById('icone_visibilite').src = "/static/images/show.png";
        visible = false;
    } else {
        document.getElementById('password').setAttribute("type", "password");
        document.getElementById('icone_visibilite').src = "/static/images/hide.png";
        visible = true;
    }
}


function passer_parametre_form(element){
    let id_element = element.parentElement.id.replace('ele-','');
    let hidden_value = document.getElementById("id-element");
    hidden_value.value = id_element;
    document.getElementById("form_email").value = document.getElementById("email-"+id_element).innerText;
    document.getElementById("form_nom").value = document.getElementById("nom-"+id_element).innerText;
    document.getElementById("form_prenom").value = document.getElementById("prenom-"+id_element).innerText;
    
    var role = document.getElementById("select_role");
    document.getElementById("select_role").options[document.getElementById("select_role").selectedIndex] = role;

    if (document.getElementById("actif-"+id_element).classList.contains("fa-check")){
        document.getElementById("form_actif").checked = true;
    } else {
        document.getElementById("form_actif").checked = false;
    }

}


function modifierLigneFormation(element) {
    // Obtenez les données de la ligne de formation
    let row = element.closest('tr');
    let intitule = row.cells[0].innerText;
    let niveauQualif = row.cells[1].innerText;
    let groupe = row.cells[2].innerText;

    // Remplissez les champs du formulaire de modification
    document.getElementById('modif_intitule').value = intitule.trim();
    document.getElementById('modif_niveau_qualif').value = niveauQualif.trim();
    document.getElementById('modif_groupe').value = groupe.trim();

    // Affichez la fenêtre modale de modification
    $('#modalModifierFormation').modal('show');
}















