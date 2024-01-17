$(function () {

  var $sunChart = $("#sun-chart");
  $.ajax({
    url: $sunChart.data("url"),
    success: function (data) {
 
      var ctx = $sunChart[0].getContext("2d");
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: [],
          datasets: [
            {
              // label: 'Fully Rounded',
              data: [],
              borderColor: 'rgba(255, 99, 132, 0.2)',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderWidth: 2,
              borderRadius: 8,
              borderSkipped: false,
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
                ticks: {
                  beginAtZero: true,
                }
              }
          },
          plugins: {
            legend: {
              position: 'top',
            },
            // title: {
            //   display: true,
            //   text: 'Chart.js Bar Chart'
            // }
          }
        }
      });
        
          for (let i=0; i< 5; i++){
            setTimeout(function() {
            myChart.data.labels.push([data.labels[i]]);
            myChart.data.datasets[0].data.push([data.data[i]]);
            myChart.update();
          }, i * 1000)
          }
        ;
      
    },
    error: () => console.log("Failed to fetch chart data from the endpoint.")
  });
  
  });
