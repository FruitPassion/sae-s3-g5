const fichePdf = document.getElementById("pdf");
fichePdf.addEventListener("click", imprimer);

function imprimer(e) {
    e.preventDefault();
    window.print();
}