function chargement_preview(element, ajout, valeur, position_element) {
    demarrer(valeur, position_element);
    changeSize(element, ajout);
}

function changement_caroussel(ajout, element) {
    ajout = parseInt(ajout);
    
    let deplacementG = document.getElementById("deplacement-gauche");
    let deplacementD = document.getElementById("deplacement-droite");

    let caroussel = document.getElementById("caroussel");
    let visibleFieldset = caroussel.querySelector("fieldset:not([hidden])");
    let visibleFieldsetNumber = parseInt(visibleFieldset.id.match(/\d+/)[0])+ajout;

    if ((element.id === "deplacement-gauche" && visibleFieldsetNumber === 0) ||
    element.id === "deplacement-droite" && visibleFieldsetNumber === 60) {
        return;
    } 

    visibleFieldset.hidden = true;
    
    if (visibleFieldsetNumber == 10) {
        deplacementG.classList.add("fdisabled");
    } else if (visibleFieldsetNumber != 10) {
        deplacementG.classList.remove("fdisabled");
    }

    if (visibleFieldsetNumber == 50) {
        // enelever class fdisabled
        deplacementD.classList.add("fdisabled");
    } else if (visibleFieldsetNumber != 50) {
        // ajouter class fdisabled
        deplacementD.classList.remove("fdisabled");
    }

    let nextFieldset = caroussel.querySelector("#field-" + (visibleFieldsetNumber));
    nextFieldset.hidden = false;
}