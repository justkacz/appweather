
$(function () {

  var $presChart = $("#pres-chart");
  $.ajax({
    url: $presChart.data("url"),
    success: function (data) {
  
      var ctx = $presChart[0].getContext("2d");
      // const colors = {
      //   purple: {
      //     default: "rgba(149, 76, 233, 1)",
      //     half: "rgba(149, 76, 233, 0.5)",
      //     quarter: "rgba(149, 76, 233, 0.25)",
      //     zero: "rgba(149, 76, 233, 0)"
      //   },
      //   indigo: {
      //     default: "rgba(80, 102, 120, 1)",
      //     quarter: "rgba(80, 102, 120, 0.25)"
      //   }
      // };
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
      gradient = ctx.createLinearGradient(0, 25, 0, 120);
      gradient.addColorStop(0, colors.purple.half);
      gradient.addColorStop(0.35, colors.purple.quarter);
      gradient.addColorStop(1, colors.purple.zero);

      new Chart(ctx, {
        type: "line",
        data: {
          labels: data.labels,
          datasets: [
            {
              fill: true,
              backgroundColor: gradient,
              pointBackgroundColor: colors.purple.default,
              borderColor: colors.purple.default,
              data: data.data,
              lineTension: 0.2,
              borderWidth: 1,
              pointRadius: 3
            }
          ]
        },
        options: {
          layout: {
            padding: {
              bottom: 5
            }
          },
          scales: {
            y: {
              title: {
                display: true,
                text: 'Pressure'
              }
            },
           x: {
              title: {
                display: true,
                text: 'Capitals'
              }
            }
          },
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            } 
          }
        }
      });
      
  
    }
  });
  
  });






// $(function () {

//   var $populationChart = $("#population-chart");
//   $.ajax({
//     url: $populationChart.data("url"),
//     success: function (data) {
  
//       var ctx = $populationChart[0].getContext("2d");
  
//       new Chart(ctx, {
//         type: 'horizontalBar',
//         data: {
//           labels: data.labels.slice(0, 7),
//           datasets: [{
//             label: 'Population',
//             backgroundColor: [
//               'rgba(255, 99, 132, 0.2)',
//               'rgba(255, 159, 64, 0.2)',
//               'rgba(255, 205, 86, 0.2)',
//               'rgba(75, 192, 192, 0.2)',
//               'rgba(54, 162, 235, 0.2)',
//               'rgba(153, 102, 255, 0.2)',
//               'rgba(201, 203, 207, 0.2)'
//             ],
//             borderColor: [
//               'rgb(255, 99, 132)',
//               'rgb(255, 159, 64)',
//               'rgb(255, 205, 86)',
//               'rgb(75, 192, 192)',
//               'rgb(54, 162, 235)',
//               'rgb(153, 102, 255)',
//               'rgb(201, 203, 207)'
//             ],
//             borderWidth: 1,
//             data: data.data.slice(0, 7)
//           }]          
//         },
//         options: {
//           responsive: true,
//           //indexAxis: 'y',
//           maintainAspectRatio: false,
//           options: {
//             scales: {
//               ticks: {   
//               y: {
//                 beginAtZero: true
//               }
//             }
//             }
//           }
//         }
//       });
  
//     }
//   });
  
//   });




