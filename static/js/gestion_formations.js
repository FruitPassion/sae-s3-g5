function confirmationSuppression(element, intitule, id_formation) {
    const formationCells = document.querySelectorAll(`#pers-${id_formation} td`);
    formationCells.forEach(cell => {
        cell.style.backgroundColor = '#F8D7DA';
    });
    
    setTimeout(() => {
        if (confirm('Voulez-vous vraiment supprimer la formation : ' + intitule + " ?")) {
            supprimerFormation(id_formation);
        } else {
            formationCells.forEach(cell => {
                cell.style.backgroundColor = '';
            });
        }
    }, 100);
}

function supprimerFormation(id_formation) {
    fetch('/admin/gestion-formation', { 
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id_formation: id_formation })
    })    
    .then(response => {
        if (response.ok) {
            window.location.reload();
        }
    })
}
