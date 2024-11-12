function changeSize(element, ajout=0){
    let style = window.getComputedStyle(element.parentElement, null).getPropertyValue('font-size');
    let fontSize = parseFloat(style);
    element.style.width = fontSize+ajout+"px";
    element.style.height = fontSize+ajout+"px";
}
function lireTexte(texte) {
    const syntheseVocale = window.speechSynthesis;
    const message = new SpeechSynthesisUtterance(texte);
    let voices = syntheseVocale.getVoices();
    message.lang = "fr-FR";
    message.voice = voices[1];
    syntheseVocale.speak(message);
}

function lireHiddenTexte(element) {
    lireTexte(element.parentElement.getElementsByTagName("a")[0].innerText);
}

function lireDate(element) {
    let valeur = element.parentElement.getElementsByTagName("input")[0].value;
    if (valeur === "") {
        valeur = "Date non renseignée ou incomplète";
    }
    lireTexte(valeur);
}

function lireTextarea(element) {
    let valeur = element.parentElement.getElementsByTagName("textarea")[0].value;
    if (valeur === "") {
        valeur = "Texte non renseigné";
    }
    lireTexte(valeur);
}

function lireTemps(element) {
    let select = element.parentElement.getElementsByTagName("select")[0];
    let selected = select.options[select.selectedIndex].text;
    selected = selected.replace("h15", "h 15 minutes");
    selected = selected.replace("h30", "h 30 minutes");
    selected = selected.replace("h45", "h 45 minutes");
    selected = selected.replace("0h", "");
    if ((!selected.includes("minutes")) && (!selected.includes("h00")))
        selected += " minutes";
    selected = selected.replace("h00", "h");
    selected = selected.replace("h ", "h et ");
    lireTexte(selected);
}

function changerSizeHiddenTexte(element) {
    let textHeight = element.parentElement.style.fontSize.valueOf();
    changeSize(element, parseInt(textHeight))
}