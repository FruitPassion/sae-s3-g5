function creation_graphique_suivi_progression_apprenti(etat_fiches) {
    var chart_suivi_progression = document.getElementById('camembert');
    var context = chart_suivi_progression.getContext('2d');
    var fiches_terminees = 0;
    var fiches_arretees = 0;
    var fiches_en_cours = 0;
    var id = Object.keys(etat_fiches);
    for (let i=0; i<id.length; i++) {
        let etat = etat_fiches[id[i]];
        if (etat === 1) {
            fiches_terminees++;
        } else if (etat === 0) {
            fiches_en_cours++;
        } else {
            fiches_arretees++;
        }
    }
    
    var chart = new Chart(context, {
        type: 'pie',
        data: {
            labels: ['Fiches terminées', 'Fiches en cours', 'Fiches arrêtées'],
            datasets: [{
                label: 'Fiches',
                data: [fiches_terminees, fiches_en_cours, fiches_arretees],
                backgroundColor: [
                    '#98FB98',
                    '#FF8B28',
                    '#C30010'
                ],
                hoverOffset: 4
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            fontFamily: 'Montserrat',
                            size: 30
                        }
                    }
                },
                datalabels: {
                    color: 'black',
                    anchor: 'center',
                    font: {
                        size: 30,
                        weight: 'bold'
                    },
                    formatter: (value, context) => {
                        return value;
                    }
                },
            },
            responsive: true,
            maintainAspectRatio: true,
        }
    });
}