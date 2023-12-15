function changer_police(){
    let selecteur_police = document.getElementById("selecteur_police");
    let police_selectionnee = selecteur_police.value;

    // changement de police (texte de test dans le html)
    let texte = document.getElementById("visualisation_texte");
    texte.style.fontFamily = police_selectionnee;

    // mise à jour de la visualisation de texte
    mettre_a_jour_texte();
}

// mise à jour du texte de visualisation
function mettre_a_jour_texte() {
    let visualisation_texte = document.getElementById("visualisation_texte");
    
    // Récupère les valeurs actuelles
    let taille_police = document.getElementById("taille_police").value + "px";
    let police = document.getElementById("selecteur_police").value;
    let couleur = document.getElementById("color_picker").value;

    if (couleur.toLowerCase() === "#ffffff"){
        visualisation_texte.style.textShadow = "2px 2px 4px #000000";
    } else {
        visualisation_texte.style.textShadow = "";
    }

    // Applique les valeurs à la visualisation du texte
    visualisation_texte.style.fontSize = taille_police;
    visualisation_texte.style.fontFamily = police;
    visualisation_texte.style.color = couleur;
}



// Visualisation de la couleur de fond
function mettre_a_jour_couleur_fond() {
    let visualisation_couleur = document.getElementById("couleur_fond");
    visualisation_couleur.style.backgroundColor = document.getElementById("color_picker").value;
}

function changer_preview(element){
    let fields = document.getElementsByTagName("fieldset");
    for (const f of fields){
        f.setAttribute("hidden", "");
    }
    document.getElementById("field-"+element.value).removeAttribute("hidden");
    let sets = document.getElementsByClassName("set-hidde");
    for (const s of sets){
        s.setAttribute("hidden", "");
    }
    document.getElementById("set-"+element.value).removeAttribute("hidden");
    document.getElementById("element-"+element.value).removeAttribute("hidden");
}

function changer_element(element){
    let sets = document.getElementsByClassName("element-hidde");
    for (const s of sets){
        s.setAttribute("hidden", "");
    }
    document.getElementById("element-"+element.value).removeAttribute("hidden");
}

