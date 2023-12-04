function changeSize(element){
    let style = window.getComputedStyle(element.parentElement, null).getPropertyValue('font-size');
    let fontSize = parseFloat(style);
    element.style.width = fontSize+"px";
}
function lireTexte(texte) {
    const syntheseVocale = window.speechSynthesis;
    const message = new SpeechSynthesisUtterance(texte);
    let voices = syntheseVocale.getVoices();
    message.lang = "fr-FR";
    message.voice = voices[1];
    syntheseVocale.speak(message);
}