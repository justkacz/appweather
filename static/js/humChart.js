
$(function () {

  var $humChart = $("#hum-chart");
  $.ajax({
    url: $humChart.data("url"),
    success: function (data) {
 
      var ctx = $humChart[0].getContext("2d");

      const colors = {
        purple: {
          default: "rgba(245, 158, 11, 1)",
          half: "rgba(245, 158, 11, 0.5)",
          quarter: "rgba(245, 158, 11, 0.25)",
          zero: "rgba(245, 158, 11, 0)"
        },
        indigo: {
          default: "rgba(80, 102, 120, 1)",
          quarter: "rgba(80, 102, 120, 0.25)"
        }
      };
      gradient = ctx.createLinearGradient(0, 25, 0, 50);
      gradient.addColorStop(0, colors.purple.half);
      gradient.addColorStop(0.35, colors.purple.quarter);
      gradient.addColorStop(1, colors.purple.zero);

      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: [],
          datasets: [
            {
              label: 'Fully Rounded',
              data: [],
              // borderColor: 'rgba(255, 99, 132, 0.2)',
              backgroundColor: gradient,
              // backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: "rgba(245, 158, 11, 0.3)",
              borderWidth: 2,
              // borderRadius: 8,
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
                  text: 'Humidity'
                }
              },
            x: {
              title: {
                display: true,
                text: 'Capitals'
              }
            }
          },
          plugins: {
            legend: {
              display: false,
              // position: 'top',
            },
            // title: {
            //   display: true,
            //   text: 'Chart.js Bar Chart'
            // }
          }
        }
      });
      // for (let i=0; i< data.data.length; i++){
      //     // console.log(data.data.length, data.labels[i], data.data[i])
      //     myChart.data.labels.push([data.labels[i]]);
      //     myChart.data.datasets[0].data.push([data.data[i]]);
      //     console.log(myChart.data.datasets[0].data, myChart.data.labels);
      //     // setInterval(myChart.update(), 3000);
      //   }
        
          for (let i=0; i< data.data.length; i++){
            setTimeout(function() {
            myChart.data.labels.push([data.labels[i]]);
            myChart.data.datasets[0].data.push([data.data[i]]);
            myChart.update();
          }, i * 1000)
          }
        ;

      // setInterval(myChart.update(), 3000);
      // myChart.update();
      
    },
    error: () => console.log("Failed to fetch chart data from the endpoint.")
  });
  
  });


