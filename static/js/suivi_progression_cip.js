function creation_graphique_suivi_progression_cip(niv_fiche) {
  var chart_suivi_progression = document.getElementById('suivi_progression_cip');
  var context = chart_suivi_progression.getContext('2d');
  const liste_niv_fiche = [];
  const liste_num_fiche = [];
  const liste_etat_fiche = [];
  for (const niveau of niv_fiche) {
    liste_niv_fiche.push(niveau["total_niveau"]);
    liste_num_fiche.push(niveau["numero"]);
    if (niveau["etat_fiche"] === 0){
      const etatEnCours = new Image(30,30);
      etatEnCours.src = "/static/images/pause.png";
      liste_etat_fiche.push(etatEnCours);
    }
    if (niveau["etat_fiche"] === 1){
      const etatFini = new Image(30,30);
      etatFini.src = "/static/images/check.png";
      liste_etat_fiche.push(etatFini);
    }
    if (niveau["etat_fiche"] === 2){
      const etatArret = new Image(30,30);
      etatArret.src = "/static/images/stop.png";
      liste_etat_fiche.push(etatArret);
    }
  }
  var line_chart = new Chart(context, {
    type: 'line',
    data: {
      labels: liste_num_fiche,
      datasets: [{
        label: "Niveau d'accessibilité totale",
        data: liste_niv_fiche,
        backgroundColor: "#533C2B",
        borderColor: "#533C2B",
        pointStyle: liste_etat_fiche, // images à la place des points
        pointRadius: 10, 
      }]
    },
    options: {
      plugins: {
        legend: {
          display: false,
        },
        zoom : {
          zoom : {
            wheel: {
              enabled: true,
            },
            pinch : {
              enabled : true
            },
            mode: 'xy',
          }
        }
      },
      responsive: true,
      hover: {
        mode: 'label',
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Numéro',
            font: {
              size: 30,
              family: 'Montserrat',
            },
          },
        },
        y: {
          title: {
            display: true,
            text: 'Niveau d\'accessibilité totale',
            font: {
              size: 30,
              family: 'Montserrat',
            },
          },
          min: 22,
          max: 66,
          ticks: {
            stepSize: 1,
          },
        },
      },
    },    
  });
  return line_chart;
}

window.onload = function () {
  var chart = creation_graphique_suivi_progression_cip(niv_fiche);

  // Ajoutez un écouteur d'événement de redimensionnement
  window.addEventListener('resize', function () {
    chart.resize();
  });
};