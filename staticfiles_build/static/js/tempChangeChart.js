
$(function () {

  var $tempChangeChart = $("#temp-change-chart");
  $.ajax({
    url: $tempChangeChart.data("url"),
    success: function (data) {

      const dane = []
      const labels = []
  
      for (let i = 1; i < data.data.length; i++) {
        dane.push(((data.data[i].temp-data.data[i-1].temp)/Math.abs(data.data[i-1].temp))*100);
        labels.push(data.data[i].measure_date);
        };

      var ctx = $tempChangeChart[0].getContext("2d");
          Chart.register(ChartDataLabels);
          
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
      gradient.addColorStop(0.8, colors.purple.quarter);
      gradient.addColorStop(1, colors.purple.zero);

      new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              fill: true,
              backgroundColor: gradient,
              pointBackgroundColor: colors.purple.default,
              borderColor: colors.purple.default,
              data: dane,
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
              ticks: {
                padding: 20
              },
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
            },
            title: {
              display: true,
              text: 'Chart.js Line Chart',
              padding: {
                bottom: 30
            }
            },
            datalabels: {
              // backgroundColor: "rgba(245, 158, 11, 1)",
              // backgroundColor: "",
              // borderRadius: 4,
              anchor: 'end',
              align: 'end',
              color: 'rgba(245, 158, 11, 1)',
              // labels: {
              //   value: {
              //     color: 'blue'
              //   }
              // },
              // font: {
              //   weight: 'bold'
              // },
              // textAlign: 'center',
              // formatter: Math.round,
              formatter: function(value, ctx) {
                // var index = ctx.dataIndex;
                // var label = ctx.chart.data.labels[index];
                // return label + '\n' + value;
                return value.toFixed(1) + '%';
              }
            },
            tooltip: {
              enabled: false
            },
          }
        }
      });
      
  
    }
  });
  
  });




// $(function () {

//   var $tempChangeChart = $("#temp-change-chart");
//   $.ajax({
//     url: $tempChangeChart.data("url"),
//     success: function (data) {

//       const dane = []
//       const labels = []
  
//       for (let i = 0; i < data.data.length; i++) {
//         dane.push(data.data[i].temp);
//         // console.log(dane);
//         labels.push(data.data[i].measure_date);
//         // console.log(labels);
//         };
//         console.log(data.data);

//       var ctx = $tempChangeChart[0].getContext("2d");
//       // const colors = {
//       //   purple: {
//       //     default: "rgba(149, 76, 233, 1)",
//       //     half: "rgba(149, 76, 233, 0.5)",
//       //     quarter: "rgba(149, 76, 233, 0.25)",
//       //     zero: "rgba(149, 76, 233, 0)"
//       //   },
//       //   indigo: {
//       //     default: "rgba(80, 102, 120, 1)",
//       //     quarter: "rgba(80, 102, 120, 0.25)"
//       //   }
//       // };
//       const colors = {
//         purple: {
//           default: "rgba(245, 158, 11, 1)",
//           half: "rgba(245, 158, 11, 0.5)",
//           quarter: "rgba(245, 158, 11, 0.25)",
//           zero: "rgba(245, 158, 11, 0)"
//         },
//         indigo: {
//           default: "rgba(80, 102, 120, 1)",
//           quarter: "rgba(80, 102, 120, 0.25)"
//         }
//       };
//       gradient = ctx.createLinearGradient(0, 25, 0, 120);
//       gradient.addColorStop(0, colors.purple.half);
//       gradient.addColorStop(0.35, colors.purple.quarter);
//       gradient.addColorStop(1, colors.purple.zero);

//       new Chart(ctx, {
//         type: "line",
//         data: {
//           labels: labels,
//           datasets: [
//             {
//               fill: true,
//               backgroundColor: gradient,
//               pointBackgroundColor: colors.purple.default,
//               borderColor: colors.purple.default,
//               data: dane,
//               lineTension: 0.2,
//               borderWidth: 1,
//               pointRadius: 3
//             }
//           ]
//         },
//         options: {
//           layout: {
//             padding: {
//               bottom: 5
//             }
//           },
//           scales: {
//             y: {
//               title: {
//                 display: true,
//                 text: 'Pressure'
//               }
//             },
//            x: {
//               title: {
//                 display: true,
//                 text: 'Capitals'
//               }
//             }
//           },
//           responsive: true,
//           maintainAspectRatio: false,
//           plugins: {
//             legend: {
//               display: false
//             } 
//           }
//         }
//       });
      
  
//     }
//   });
  
//   });






