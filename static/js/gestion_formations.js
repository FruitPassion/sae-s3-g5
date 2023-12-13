function confirmationSuppression(element, intitule, id_formation) {
    if (confirm('Voulez-vous vraiment supprimer la formation : ' + intitule + " ?")) {
        supprimerFormation(id_formation);
    }
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
