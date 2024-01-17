function chargement_preview(element, ajout, valeur, position_element) {
    demarrer(valeur, position_element);
    changeSize(element, ajout);
}

function changement_caroussel(ajout, element) {
    let avancee = document.getElementById("avancee");
    ajout = parseInt(ajout);

    let caroussel = document.getElementById("caroussel");
    let visibleFieldset = caroussel.querySelector("fieldset:not([hidden])");
    let visibleFieldsetNumber = parseInt(visibleFieldset.id.match(/\d+/)[0])+ajout;

    if ((element.id === "deplacement-gauche" && visibleFieldsetNumber < 0) ||
    element.id === "deplacement-droite" && visibleFieldsetNumber === 90) {
        return;
    } 

    visibleFieldset.hidden = true;

    gererFleches(visibleFieldsetNumber);

    let nextFieldset = caroussel.querySelector("#field-" + (visibleFieldsetNumber));
    nextFieldset.hidden = false;
    avancee.value = nextFieldset.id.match(/\d+/)[0];
}

function gererFleches(visibleFieldsetNumber) {

    let deplacementG = document.getElementById("deplacement-gauche");
    let deplacementD = document.getElementById("deplacement-droite");

    if (visibleFieldsetNumber === "00") {
        deplacementG.classList.add("fdisabled");
    } else if (visibleFieldsetNumber !== "00") {
        deplacementG.classList.remove("fdisabled");
    }

    if (visibleFieldsetNumber === 80) {
        // enelever class fdisabled
        deplacementD.classList.add("fdisabled");
    } else if (visibleFieldsetNumber !== 80) {
        // ajouter class fdisabled
        deplacementD.classList.remove("fdisabled");
    }
}

function displaySelectedImage(event, elementId) {
    const selectedImage = document.getElementById(elementId);
    const fileInput = event.target;

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            selectedImage.src = e.target.result;
        };

        reader.readAsDataURL(fileInput.files[0]);
    }
}