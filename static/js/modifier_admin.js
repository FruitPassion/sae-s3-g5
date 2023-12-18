let visible = true;

function visibilite() {
    if (visible) {
        document.getElementById('password').setAttribute("type", "text");
        document.getElementById('icone_visibilite').src = "{{ url_for('static', filename='images/show.png') }}";
        visible = false;
    } else {
        document.getElementById('password').setAttribute("type", "password");
        document.getElementById('icone_visibilite').src = "{{ url_for('static', filename='images/hide.png') }}";
        visible = true;
    }
}

let editionEnCoursPersonnel = false;

function modifierLignePersonnel(button) {

    if (!editionEnCoursPersonnel) {
        editionEnCoursPersonnel = true; // Passe en mode édition
        let ligne = button.parentNode.parentNode;
        let colonnes = ligne.getElementsByTagName('td');

        for (let i = 0; i < 6; i++) {
            switch (i) {
                case 0:
                    break;
                case 4:
                    var valeurActuelle = colonnes[i].innerText;

                    // Crée une liste déroulante avec des options
                    var select = document.createElement('select');
                    var option1 = document.createElement('option');
                    option1.value = 'Educateur';
                    option1.text = 'Educateur';
                    var option2 = document.createElement('option');
                    option2.value = 'Educateur Administrateur';
                    option2.text = 'Educateur Administrateur';

                    // Sélectionne l'option correspondant à la valeur actuelle
                    if (valeurActuelle === 'Educateur') {
                        option1.selected = true;
                    } else {
                        option2.selected = true;
                    }

                    // Ajoute les options à la liste déroulante
                    select.appendChild(option1);
                    select.appendChild(option2);

                    // Remplace le contenu de la colonne par la liste déroulante
                    colonnes[i].innerHTML = '';
                    colonnes[i].appendChild(select);
                    break;
                case 5:
                    // Crée une checkbox pour l'état "Actif"
                    var checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.checked = valeurActuelle;

                    // Remplace le contenu de la colonne par la case à cocher
                    colonnes[5].innerHTML = '';
                    colonnes[5].appendChild(checkbox);
                    break;
                default:
                    var valeurActuelle = colonnes[i].innerText;
                    colonnes[i].innerHTML = `<input type="text" value=" ${valeurActuelle} " id=" ${colonnes[i]} ">`;
            }
        }
        var bouton = ligne.getElementsByTagName('button')[0];
        bouton.innerText = 'Enregistrer';
        bouton.setAttribute('onclick', 'enregistrerLignePersonnel(this)');
    }
}

function enregistrerLignePersonnel(button) {
    if (editionEnCoursPersonnel) {
        editionEnCoursPersonnel = false;
        let ligne = button.parentNode.parentNode;
        let colonnes = ligne.getElementsByTagName('td');

        // Après avoir sauvegardé les modifications, remplacement des champs modifiables par des éléments HTML
        for (let i = 0; i < 6; i++) {
            switch (i) {
                case 0:
                    // Ne fait rien pour la première colonne (index 0)
                    break;
                case 4: // Colonne "Role"
                    var nouvelleValeur = colonnes[i].getElementsByTagName('select')[0].value; // Récupère la nouvelle valeur après la modification

                    // Remplace le select par le texte
                    colonnes[i].innerText = nouvelleValeur;
                    break;
                case 5: // Colonne "Actif"
                    var nouvelleValeur = colonnes[i].getElementsByTagName('input')[0].checked;

                    // Remplacez la checkbox par l'image corrspondante
                    colonnes[i].innerHTML = nouvelleValeur ? '<i class="fa fa-check"></i>' : '<i class="fa fa-times"></i>';
                    break;
                default: // Pour les autres colonnes
                    var nouvelleValeur = colonnes[i].getElementsByTagName('input')[0].value;

                    colonnes[i].innerText = nouvelleValeur;
                    break;
            }
        }

        let bouton = ligne.getElementsByTagName('button')[0];
        bouton.innerHTML = `<i class="fa fa-pencil-square-o" aria-hidden="true"></i>`;
        bouton.setAttribute('onclick', 'modifierLignePersonnel(this)');
    }
}

editionEnCoursApprenti = false;
function modifierLigneApprenti(button) {

    if (!editionEnCoursApprenti){
        editionEnCoursApprenti = true; // Passe en mode édition
        var ligne = button.parentNode.parentNode;
        var colonnes = ligne.getElementsByTagName('td');
    
        for (var i = 0; i < 5; i++) {

            switch(i) {
                case 0: break;
                /*
                case 3:
                    var imageActuelle = colonnes[i].getElementsByTagName('img')[0].src;

                    // Crée un champ input de type 'file' pour l'image
                    var inputImage = document.createElement('input');
                    inputImage.type = 'file';
                    inputImage.className = "form-control fs-1 my-3";
                    inputImage.accept = 'image/png, image/jpeg, image/jpg'; // N'accepte que les fichiers image
                
                    colonnes[i].innerHTML = ''; // Efface le contenu actuel
                    colonnes[i].appendChild(inputImage);

                    // Affiche l'image actuelle (ou charge une image par défaut si aucune n'est définie)
                    var imageElement = document.createElement('img');

                    imageElement.src = imageActuelle || "{{ url_for('static', filename='images/photo_profile/defaut_profile.png') }}";
                    colonnes[i].appendChild(imageElement);
                    break;
                */
                case 4:
                    // Crée une checkbox pour l'état "Actif"
                    var checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = 'actif';
                    checkbox.checked = valeurActuelle;
        
                    // Remplacer le contenu de la colonne par la case à cocher
                    colonnes[4].innerHTML = '';
                    colonnes[4].appendChild(checkbox);
                    break;
                default:
                    var valeurActuelle = colonnes[i].innerText;
                    colonnes[i].innerHTML = `<input type="text" value=" ${valeurActuelle} " id=" ${colonnes[i]} ">`;
            }
        }
        let bouton = ligne.getElementsByTagName('button')[0];
        bouton.innerText = 'Enregistrer';
        bouton.setAttribute('onclick', 'enregistrerLigneApprenti(this)');
    }

}

function enregistrerLigneApprenti(button) {
    if (editionEnCoursApprenti) {
        editionEnCoursApprenti = false; 
        var ligne = button.parentNode.parentNode;
        var colonnes = ligne.getElementsByTagName('td');
        
        // Après avoir sauvegardé les modifications, remplacement des champs modifiables par des éléments HTML
        for (var i = 0; i < 5 ; i++) {
            switch (i) {
                case 0:
                    // récupère la nouvelle valeur de la colonne nom
                    var nom = colonnes[i+1].getElementsByTagName('input')[0].value.trim();;
                    colonnes[i+1].innerText = nom;  

                    // récupère la nouvelle valeur de la colonne prénom
                    var prenom = colonnes[i+2].getElementsByTagName('input')[0].value.trim();;
                    colonnes[i+2].innerText = prenom; 

                    // met à jour la colonne login
                    let deuxPremieresLettresPrenom = prenom.substring(0, 2).toUpperCase();
                    let premiereLettreNom = nom.charAt(0).toUpperCase();
                    let longueurNomPrenom = nom.length + prenom.length;
                    var login = deuxPremieresLettresPrenom + premiereLettreNom + longueurNomPrenom;
                    colonnes[i].innerText = login;

                    break;
                /*
                case 3: // Colonne "Photo"
                    var imageElement = input.parentNode.getElementsByTagName('img')[0];
                    var file = input.files[0]; // Récupérer le fichier image sélectionné
                
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        imageElement.src = e.target.result; // Afficher la nouvelle image
                    }
                    reader.readAsDataURL(file); // Lire le fichier en tant qu'URL
                    break;
                */
                case 4: // Colonne "Actif"
                    var checkbox = colonnes[i].getElementsByTagName('input')[0];
                    var nouvelleValeur = checkbox.checked;
                    colonnes[i].innerHTML = nouvelleValeur ? '<i class="fa fa-check"></i>' : '<i class="fa fa-times"></i>';
                    break;
                
                default: // Pour les autres colonnes
                    var nouvelleValeur = colonnes[i].getElementsByTagName('input')[0].value;
                    colonnes[i].innerText = nouvelleValeur;     
            }
        }

        let bouton = ligne.getElementsByTagName('button')[0];
        bouton.innerHTML = '<i class="fa fa-pencil-square-o" aria-hidden="true"></i>';
        bouton.setAttribute('onclick', 'modifierLigneApprenti(this)');
    }
}