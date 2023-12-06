function creation_graphique_suivi_progression_cip(niv_fiche) {
  var chart_suivi_progression = document.getElementById('suivi_progression_cip');
  var context = chart_suivi_progression.getContext('2d');
  const liste_niv_fiche = [0];
  const liste_num_fiche = [0];
  for (const niveau of niv_fiche) {
    liste_niv_fiche.push(niveau["total_niveau"]);
    liste_num_fiche.push(niveau["numero"]);
  }

  var line_chart = new Chart(context, {
    type: 'line',
    data: {
      labels: liste_num_fiche,
      datasets: [{
        label: 'Nombre de fiches créées',
        // jeu de données random - à remplacer par les données de la BDD
        data: liste_niv_fiche,
        backgroundColor: "#000",
        borderColor: "#000"
      }]
    },
    options: {
      responsive: true,
      title: {
        display: true,
        text: 'Nombre de fiches créées par jour'
      }
    }
  });
}