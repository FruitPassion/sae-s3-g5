function changer_police(){
    var selecteur_police = document.getElementById("selecteur_police");
    var police_selectionnee = selecteur_police.value;

    // changement de police (texte de test dans le html)
    var texte = document.getElementById("visualisation_texte");
    texte.style.fontFamily = police_selectionnee;

    // mise à jour de la visualisation de texte
    mettre_a_jour_texte();
}

// mise à jour du texte de visualisation
function mettre_a_jour_texte() {
    var visualisation_texte = document.getElementById("visualisation_texte");
    
    // Récupère les valeurs actuelles
    var taille_police = document.getElementById("taille_police").value + "px";
    var police = document.getElementById("selecteur_police").value;
    var couleur = document.getElementById("color_picker").value;

    // Applique les valeurs à la visualisation du texte
    visualisation_texte.style.fontSize = taille_police;
    visualisation_texte.style.fontFamily = police;
    visualisation_texte.style.color = couleur;
}

// Clic sur le bouton "Suivant" de la page "personnaliser_fiche_texte_champs.html"
document.getElementById("bouton_suivant").addEventListener("click", function() {
    window.location.href = "personnel/personnaliser_fiche_couleur_fond.html"; });

// Visualisation de la couleur de fond
function mettre_a_jour_couleur_fond() {
    var visualisation_couleur = document.getElementById("couleur_fond");
    var couleur = document.getElementById("color_picker").value;
    visualisation_couleur.style.backgroundColor = couleur;
}