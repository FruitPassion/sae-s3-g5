function creation_graphique_suivi_progression_cip(niv_fiche, etat_fiches) {
  var chart_suivi_progression = document.getElementById('suivi_progression_cip');
  var context = chart_suivi_progression.getContext('2d');
  const liste_niv_fiche = [];
  const liste_num_fiche = [];
  for (const niveau of niv_fiche) {
    liste_niv_fiche.push(niveau["total_niveau"]);
    liste_num_fiche.push(niveau["numero"]);
  }
  const liste_etat_fiche = [];
  for (const etat of etat_fiches) {
    if (etat === 0){
      const etatEnCours = new Image();
      etatEnCours.src = "/static/images/pause.png";
      liste_etat_fiche.push(etatEnCours);
    }
    if (etat === 1){
      const etatFini = new Image();
      etatFini.src = "/static/images/check.png";
      liste_etat_fiche.push(etatFini);
    }
    if (etat === 2){
      const etatArret = new Image();
      etatArret.src = "/static/images/stop.png";
      liste_etat_fiche.push(etatArret);
    }
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
        elements:{
          point:{
            pointStyle: liste_etat_fiche,
          }
        },
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
          max: 66,
          ticks: {
            stepSize: 1,
          },
        },
      },
    },    
  });
}