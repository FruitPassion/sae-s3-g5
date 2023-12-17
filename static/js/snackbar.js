function afficher_snack(texte, type) {
  let x = document.getElementById("snackbar");
  x.innerHTML = texte;
  if (type === "success") {
    x.style.backgroundColor = "#4CAF50";
  } else if (type === "error") {
    x.style.backgroundColor = "#f44336";
  } else {
    x.style.backgroundColor = "#2196F3";
  }

  x.className = "show";

  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}