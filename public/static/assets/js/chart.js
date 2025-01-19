var options = {
    chart: {
        type: 'bar',
        height: 250
      },
      series: [{
        data: [{
          x: 'category A',
          y: 10
        }, {
          x: 'category B',
          y: 18,
          fillColor: '#EB8C87',
         strokeColor: '#C23829'
        }, {
          x: 'category C',
          y: 13
        }]
      }],
      plotOptions: {
        bar: {
          distributed: true
        }
      }  
  }
  
  var chart = new ApexCharts(document.querySelector("#barChart"), options);
  
  chart.render();