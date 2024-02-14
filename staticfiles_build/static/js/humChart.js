$(function () {

  var $humChart = $("#hum-chart");
  $.ajax({
    url: $humChart.data("url"),
    success: function (data) {
 
      var ctx = $humChart[0].getContext("2d");

      const colors = {
        yellow: {
          default: "rgba(245, 158, 11, 1)",
          half: "rgba(245, 158, 11, 0.5)",
          quarter: "rgba(245, 158, 11, 0.25)",
          zero: "rgba(245, 158, 11, 0)"
        }
      };
      gradient = ctx.createLinearGradient(0, 25, 0, 50);
      gradient.addColorStop(0, colors.yellow.half);
      gradient.addColorStop(0.35, colors.yellow.quarter);
      gradient.addColorStop(1, colors.yellow.zero);

      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: [],
          datasets: [
            {
              label: 'Fully Rounded',
              data: [],
              backgroundColor: gradient,
              borderColor: "rgba(245, 158, 11, 0.3)",
              borderWidth: 2,
              borderSkipped: false,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
                ticks: {
                  beginAtZero: true,
                },
                title: {
                  display: true,
                  text: 'Humidity %'
                }
              },
            x: {
              title: {
                display: true,
                text: 'Capitals'
              },
              ticks: {
                autoSkip: false,
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              callbacks: {
                  title: function(tooltipItem) {
                      let title = data.labels[tooltipItem[0].dataIndex];
                      return title;
                  },
                  label: function(context) {
                      let label = "Humidity: " + context.parsed.y
                      return label;
                  }
              }
          }
          }
        }
      });
          for (let i=0; i< data.data.length; i++){
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


