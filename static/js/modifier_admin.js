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
    let hidden_value = document.getElementById("id-element-"+nom_form);
    hidden_value.value = id_element;

    switch(nom_form){
        case "personnel":
            set_nom_prenom(id_element);
            document.getElementById("email_personnel").value = document.getElementById("email-"+id_element).innerText;
        
            let roles       = document.getElementById("nouveau_role");
            let ancienRole  = document.getElementById("role-" + id_element).innerText;
            ancienRole      = ancienRole.replace(" ", "_");

            for (let i = 0; i < roles.length ; i++) {
                if (roles.options[i].value === ancienRole) {
                    roles[i].setAttribute("selected", "selected");
                    break; // Sortie de la boucle une fois l'option trouvée
                }
            }
            break;

        case "apprenti":
            set_nom_prenom(id_element)
            break;

        case "admin":
            set_nom_prenom(id_element)
            document.getElementById("mail_admin").value   = document.getElementById("email-"+id_element).innerText;
            document.getElementById("nom_admin").value    = document.getElementById("nom-"+id_element).innerText;
            document.getElementById("prenom_admin").value = document.getElementById("prenom-"+id_element).innerText;
            break;

        case "formation":
            document.getElementById("form_intitule").value      = document.getElementById("intitule-"+id_element).innerText;
            document.getElementById("form_niveau_qualif").value = document.getElementById("niveau_qualif-"+id_element).innerText;
            document.getElementById("form_groupe").value        = document.getElementById("groupe-"+id_element).innerText;
            break;
        
        case "cours":
            document.getElementById("form_theme").value       = document.getElementById("theme-"+id_element).innerText;
            document.getElementById("form_cours").value       = document.getElementById("cours-"+id_element).innerText;
            document.getElementById("form_duree").value       = document.getElementById("duree-"+id_element).innerText;
            document.getElementById("select_formation").value = document.getElementById("formation-"+id_element).innerText;
            break;

        case "materiel":
            document.getElementById("form_modifier_nom").value         = document.getElementById("nom-"+id_element).innerText;
            document.getElementById("form_modifier_categorie").value   = document.getElementById("categorie-"+id_element).innerText;
            break;
    }
}

function set_nom_prenom(id_element){
    document.getElementById("form_nom").value    = document.getElementById("nom-"+id_element).innerText;
    document.getElementById("form_prenom").value = document.getElementById("prenom-"+id_element).innerText;

    if (document.getElementById("actif-"+id_element).classList.contains("fa-check")){
        document.getElementById("form_actif").checked = true;
    } else {
        document.getElementById("form_actif").checked = false;
    }
}
