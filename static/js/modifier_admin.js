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

let editionEnCours = false;

function modifierLigne(button) {

    if (!editionEnCours) {
        editionEnCours = true; // Passe en mode édition
        let ligne = button.parentNode.parentNode;
        let colonnes = ligne.getElementsByTagName('td');

        for (let i = 0; i < colonnes.length - 1; i++) {
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

                    // Remplacer le contenu de la colonne par la case à cocher
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
        bouton.setAttribute('onclick', 'enregistrerLigne(this)');
    }

}

function enregistrerLigne(button) {
    if (editionEnCours) {
        editionEnCours = false;
        let ligne = button.parentNode.parentNode;
        let colonnes = ligne.getElementsByTagName('td');

        // Après avoir sauvegardé les modifications, remplacement des champs modifiables par des éléments HTML
        for (let i = 0; i < colonnes.length - 1; i++) {
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
        bouton.setAttribute('onclick', 'modifierLigne(this)');
    }
}