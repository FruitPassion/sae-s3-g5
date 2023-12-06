function creation_graphique_suivi_progression_cip() {
  var chart_suivi_progression = document.getElementById('suivi_progression_cip');
  var context = chart_suivi_progression.getContext('2d');

  var bar_chart = new Chart(context, {
    type: 'bar',
    data: {
      labels: ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
      datasets: [{
        label: 'Nombre de fiches créées',
        // jeu de données random
        data: [3, 10, 5, 2, 7],
        backgroundColor: ["#ffcd56", "#ff6384", "#36a2eb", "#fd6b19", "#4bc0c0"],
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Nombre de fiches créées par jour'
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
            size: 25
          }
        }]
      }
    }
  });
}

window.onload = function() {
  creation_graphique_suivi_progression_cip();
}