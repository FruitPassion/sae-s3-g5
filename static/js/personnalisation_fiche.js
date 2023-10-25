function changer_police(){
    var selecteur_police = document.getElementById("selecteur_police");
    var police_selectionnee = selecteur_police.value;

    // changement de police (texte de test dans le html)
    var texte = document.getElementById("visualisation_texte");
    texte.style.fontFamily = police_selectionnee;

    // mise à jour de la visualisation de texte
    mettre_a_jour_texte();
}

function changer_couleur(){
    var hexa = document.getElementById("couleur_police_hex").value;
    var couleur = document.getElementById("visualisation_couleur");
    var rvb = document.getElementById("RVB");

    // vérification si le code hexadécimal est valide
    // (me demandez pas j'ai cherché sur ChatGPT)
    if (/^#[0-9A-Fa-f]{6}$/.test(hexa)){
        couleur.style.backgroundColor = hexa;

        // conversion hexadécimal -> RVB
        var code_hex = hexa.substring(1);
        var decimale = parseInt(code_hex, 16); // version décimale du code hexadécimal
        var r = (decimale >> 16) & 255;
        var v = (decimale >> 8) & 255;
        var b = decimale & 255;

        // mise à jour de l'affichage des valeurs RVB
        document.getElementById("rouge").innerText = r;
        document.getElementById("vert").innerText = v;
        document.getElementById("bleu").innerText = b;

        // mise à jour de la visualisation de texte
        mettre_a_jour_texte();
    } else {
        // si le code hexadécimal n'est pas valide, on affiche du blanc
        couleur.style.backgroundColor = "white";
    }
}

// mise à jour du texte de visualisation
function mettre_a_jour_texte() {
    var visualisation_texte = document.getElementById("visualisation_texte");
    
    // Récupère les valeurs actuelles
    var taille_police = document.getElementById("taille_police").value + "px";
    var police = document.getElementById("selecteur_police").value;
    var couleur = document.getElementById("couleur_police_hex").value;

    // Applique les valeurs à la visualisation du texte
    visualisation_texte.style.fontSize = taille_police;
    visualisation_texte.style.fontFamily = police;
    visualisation_texte.style.color = couleur;
}