function chargement_preview(element, ajout, valeur, position_element) {
    demarrer(valeur, position_element);
    changeSize(element, ajout);
}


function changer_preview(element) {
    let fields = document.getElementsByTagName("fieldset");
    for (const f of fields) {
        f.setAttribute("hidden", "");
    }
    document.getElementById("field-" + element.value).removeAttribute("hidden");
    let sets = document.getElementsByClassName("set-hidde");
    for (const s of sets) {
        s.setAttribute("hidden", "");
    }
    document.getElementById("set-" + element.value).removeAttribute("hidden");
    document.getElementById("element-" + element.value).removeAttribute("hidden");
}

function changer_element(element) {
    let sets = document.getElementsByClassName("element-hidde");
    for (const s of sets) {
        s.setAttribute("hidden", "");
    }
    document.getElementById("element-" + element.value).removeAttribute("hidden");
}


function get_selecteur_element(position_element) {
    return document.getElementById("selecteur-element-" + position_element).options;
}

function changer_niveau_categorie(position_element) {
    // Récupère la valeur du sélecteur de niveau
    let selecteur_niveau = document.getElementById("selecteur-niveau-" + position_element).value;
    // Récupère les options du sélecteur d'élément
    let selecteur_element = get_selecteur_element(position_element);

    // Pour chaque option du sélecteur d'élément
    for (let i = 1, iLen = selecteur_element.length; i < iLen; i++) {
        // Si le sélecteur de niveau est différent de 0
        if (selecteur_niveau !== "0") {
            // Désactiver l'option du sélecteur d'éléments
            selecteur_element[i].setAttribute("disabled", "");

            // Activer les options de personnalisation
            for (const r of ["selecteur-police-", "taille-police-", "couleur-police-", "taille-picto-",
                "couleur-picto-"]) {
                document.getElementById(r + position_element).removeAttribute("disabled");
            }
            // Activer les div de personnalisation
            for (const r of ["div-text-", "div-picto-"]) {
                document.getElementById(r + position_element).classList.remove("disabled-text");
            }

            // Appliquer les valeurs du sélecteur de niveau au sélecteur d'éléments
            document.getElementById("selecteur-niveau-" + selecteur_element[i].value).value = selecteur_niveau;
            changer_niveau_individuel(selecteur_element[i].value)
        } else {
            // Activer l'option du sélecteur d'éléments
            selecteur_element[i].removeAttribute("disabled");

            // Désactiver les options de personnalisation
            for (const r of ["selecteur-police-", "taille-police-", "couleur-police-", "taille-picto-", "couleur-picto-"]) {
                document.getElementById(r + position_element).setAttribute("disabled", "");
            }

            // Désactiver les div de personnalisation
            for (const r of ["div-text-", "div-picto-"]) {
                document.getElementById(r + position_element).classList.add("disabled-text");
            }
        }
    }
}

function changer_niveau_individuel(position_element) {
    let selecteur_niveau = document.getElementById("selecteur-niveau-" + position_element).value;
    switch (selecteur_niveau) {
        case "1":
            document.getElementById("label-" + position_element).setAttribute("hidden", "");
            document.getElementById("icone-" + position_element).removeAttribute("hidden");
            break;
        case "2":
            document.getElementById("label-" + position_element).removeAttribute("hidden");
            document.getElementById("icone-" + position_element).removeAttribute("hidden");
            break;
        case "3":
            document.getElementById("label-" + position_element).removeAttribute("hidden");
            document.getElementById("icone-" + position_element).setAttribute("hidden", "");
            break;
    }
}

function changer_texte_categorie(position_element) {
    // Récupère les options du sélecteur d'élément
    let selecteur_element = get_selecteur_element(position_element);

    // Pour chaque option du sélecteur d'élément
    for (let i = 1, iLen = selecteur_element.length; i < iLen; i++) {
        document.getElementById("selecteur-police-" + selecteur_element[i].value).value = document.getElementById("selecteur-police-" + position_element).value;
        document.getElementById("taille-police-" + selecteur_element[i].value).value = document.getElementById("taille-police-" + position_element).value;
        document.getElementById("couleur-police-" + selecteur_element[i].value).value = document.getElementById("couleur-police-" + position_element).value;
        changer_texte_individuel(selecteur_element[i].value);
    }
}

function changer_texte_individuel(position_element) {
    let label_element = document.getElementById("label-" + position_element);
    label_element.style.fontFamily = document.getElementById("selecteur-police-" + position_element).value;
    label_element.style.fontSize = document.getElementById("taille-police-" + position_element).value + "px";
    label_element.style.color = document.getElementById("couleur-police-" + position_element).value;
}

function changer_fond_categorie(position_element) {
    document.getElementById("field-" + position_element).style.backgroundColor = document.getElementById("couleur-fond-" + position_element).value;
}

function changer_icone_categorie(position_element) {
    // Récupère les options du sélecteur d'élément
    let selecteur_element = get_selecteur_element(position_element);

    // Pour chaque option du sélecteur d'élément
    for (let i = 1, iLen = selecteur_element.length; i < iLen; i++) {
        document.getElementById("couleur-picto-" + selecteur_element[i].value).value = document.getElementById("couleur-picto-" + position_element).value;
        document.getElementById("taille-picto-" + selecteur_element[i].value).value = document.getElementById("taille-picto-" + position_element).value;
        changer_icone_individuelle(selecteur_element[i].value);
    }
}

function changer_picto(position_element) {
    let element = document.getElementById("selecteur-picto-" + position_element);
    document.getElementById("icone-" + position_element).src = "/static/images/icone_fiches/" + element.value;
    changer_icone_individuelle(position_element);
}


function changer_icone_individuelle(position_element) {
    let couleur = document.getElementById("couleur-picto-" + position_element).value;
    demarrer(couleur, position_element);

    let icone_element = document.getElementById("icone-" + position_element);
    changeSize(icone_element, parseInt(document.getElementById("taille-picto-" + position_element).value));
}