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

