import { Chart } from 'chart.js';

var doc = document.getElementById('suivi_progression_cip');

const data = {
  datasets: [{
    label: 'Suivi de progression',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [0, 10, 5, 2, 20, 30, 45],
  }]
};

const config = {
  type: 'line',
  data: data,
};

var myChart = new Chart(doc, config);