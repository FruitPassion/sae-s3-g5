function creation_graphique_suivi_progression_cip(niv_fiche) {
  var chart_suivi_progression = document.getElementById('suivi_progression_cip');
  var context = chart_suivi_progression.getContext('2d');
  const liste_niv_fiche = [];
  const liste_num_fiche = [];
  for (const niveau of niv_fiche) {
    liste_niv_fiche.push(niveau["total_niveau"]);
    liste_num_fiche.push(niveau["numero"]);
  }

  var line_chart = new Chart(context, {
    type: 'line',
    data: {
      labels: liste_num_fiche,
      datasets: [{
        label: "Niveau total",
        data: liste_niv_fiche,
        backgroundColor: "#533C2B",
        borderColor: "#533C2B"
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Niveau total des fiches',
          font: {
            size: 50,
            fontFamily: 'Montserrat',
          },
        },
        legend: {
          display: false,
        },
      },
      responsive: true,
      hover: {
        mode: 'label',
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Numéro de la fiche',
            font: {
              size: 30,
              family: 'Montserrat',
            },
          },
        },
        y: {
          title: {
            display: true,
            text: 'Niveau total',
            font: {
              size: 30,
              family: 'Montserrat',
            },
          },
          max: 70,
          ticks: {
            stepSize: 1,
          },
        },
      },
    },    
  });
}