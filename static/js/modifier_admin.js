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


function passer_parametre_form(element, nom_form){
    let id_element = element.parentElement.id.replace('ele-','');
    let hidden_value = document.getElementById("id-element");
    hidden_value.value = id_element;
    document.getElementById("form_nom").value = document.getElementById("nom-"+id_element).innerText;
    document.getElementById("form_prenom").value = document.getElementById("prenom-"+id_element).innerText;
    if (document.getElementById("actif-"+id_element).classList.contains("fa-check")){
        document.getElementById("form_actif").checked = true;
    } else {
        document.getElementById("form_actif").checked = false;
    }

    if (nom_form === "personnel"){
        document.getElementById("form_email").value = document.getElementById("email-"+id_element).innerText;
        
        let roles = document.getElementById("nouveau_role");
        let ancienRole = document.getElementById("role-" + id_element).innerText;
        
        ancienRole = ancienRole.replace(" ", "_");

        for (let i = 0; i < roles.length ; i++) {
            if (roles.options[i].value === ancienRole) {
                roles[i].setAttribute("selected", "selected");
                break; // Sortie de la boucle une fois l'option trouvée
            }
        }
    }

    else if(nom_form === "apprenti"){
        document.getElementById("avatar").value = document.getElementById("photo-"+id_element).innerText;
    }

    else if (nom_form === "admin"){
        document.getElementById("mail_admin").value = document.getElementById("email-"+id_element).innerText;
        document.getElementById("nom_admin").value = document.getElementById("nom-"+id_element).innerText;
        document.getElementById("prenom_admin").value = document.getElementById("prenom-"+id_element).innerText;
        
    }
    
}
