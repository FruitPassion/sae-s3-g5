window.onload = function() {
    let fichePdf = document.getElementsByTagName("button")[0];
    fichePdf.addEventListener("click", imprimer);
}

function imprimer(e) {
    e.preventDefault();
    window.print();
}