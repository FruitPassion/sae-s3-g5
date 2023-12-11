function creation_graphique_suivi_progression_cip(etat_fiches) {
    var chart_suivi_progression = document.getElementById('camembert');
    var context = chart_suivi_progression.getContext('2d');
    const fiches_terminees = 0;
    const fiches_arretees = 0;
    const fiches_en_cours = 0;
    for (const etat of etat_fiches) {
        if (etat === "1") {
            fiches_terminees++;
        } else if (etat === "2") {
            fiches_en_cours++;
        } else {
            fiches_arretees++;
        }
    }

    var chart = new Chart(context, {
        type: 'doughnut',
        data: {
            labels: ['Fiches terminées', 'Fiches en cours', 'Fiches arrêtées'],
            datasets: [{
                label: 'Fiches',
                data: [fiches_terminees, fiches_en_cours, fiches_arretees],
                backgroundColor: [
                    'rgb(0, 255, 0)',
                    'rgb(255, 255, 0)',
                    'rgb(255, 0, 0)'
                ],
                hoverOffset: 4
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            fontFamily: 'Montserrat',
                            size: 20
                        }
                    }
                }
            }
        }
    });