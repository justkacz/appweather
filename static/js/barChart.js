

$(function () {

  var $populationChart = $("#population-chart");
  $.ajax({
    url: $populationChart.data("url"),
    success: function (data) {
  
      var ctx = $populationChart[0].getContext("2d");

      const colors = {
        purple: {
          default: "rgba(237, 164, 5, 1)",
          half: "rgba(237, 164, 5, 0.5)",
          quarter: "rgba(237, 164, 5, 0.25)",
          zero: "rgba(237, 164, 5, 0)"
        },
        indigo: {
          default: "rgba(80, 102, 120, 1)",
          quarter: "rgba(80, 102, 120, 0.25)"
        }
      };
      // const colors = {
      //   purple: {
      //     default: "rgba(245, 158, 11, 1)",
      //     half: "rgba(245, 158, 11, 0.5)",
      //     quarter: "rgba(245, 158, 11, 0.25)",
      //     zero: "rgba(245, 158, 11, 0)"
      //   },
      //   indigo: {
      //     default: "rgba(80, 102, 120, 1)",
      //     quarter: "rgba(80, 102, 120, 0.25)"
      //   }
      // };

      gradient = ctx.createLinearGradient(0, 0, 200, 0);
      gradient.addColorStop(0, colors.purple.zero);
      gradient.addColorStop(data.cloudcover.slice(0,1) * 0.01, colors.purple.quarter);
      // gradient.addColorStop(0.02, colors.purple.quarter);
      gradient.addColorStop(1, colors.purple.half);

      const innerLabel = {
        id: 'innerLabel',
        afterDatasetDraw(chart, args, pluginOptions) {
          const { ctx } = chart;
          const meta = args.meta;
          const xCoor = meta.data[0].x;
          const yCoor = meta.data[0].y;
          const perc = chart.data.datasets[0].data[0] / meta.total * 100;
          ctx.save();
          ctx.textAlign = 'center';
          ctx.font = '25px sans-serif';
          ctx.fillStyle = "rgb(245, 245, 244)";
          ctx.fillText(data.cloudcover.slice(0,1) + '%', xCoor, yCoor);
          ctx.restore();
        },
      };
          
      
      new Chart(ctx, {
        type: 'doughnut',
        plugins: [innerLabel],
        data: {
            // labels: ['Score', 'Grey Area'],
            datasets: [{
                data: [data.cloudcover.slice(0,1), 100-data.cloudcover.slice(0,1)],
                // data: [80, 20],
                backgroundColor: [
                   gradient,
                  // 'rgba(0, 0, 0, 0.2)'
                  "rgba(41, 37, 36, 0.2)"
                  // "rgba(128, 182, 244, 0.6)"
                ],
                borderColor: [
                  gradient,
                  "rgba(41, 37, 36, 0.8)"
                ],
                hoverOffset: 4
            }]
        },
        options: {
          responsive: true,
          // maintainAspectRatio: false,
          rotation: 270, // start angle in degrees
          circumference: 180, // sweep angle in degrees
          cutout: '80%',
          borderRadius: 10,
          aspectRatio: 2.5,
          plugins: {
            legend: {
              display: false,
              // position: 'top',
            },
            tooltip: {
              // enabled: false,
              // position: 'top',
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
//         type: 'doughnut',

//         data: {
//             labels: ['Score', 'Grey Area'],
//             datasets: [{
//                 data: [650, 200],
//                 backgroundColor: [
//                   "rgba(255, 26, 104, 0.2)",
//                   'rgba(0, 0, 0, 0.2)'
//                   // "rgba(128, 182, 244, 0.6)"
//                 ],
//                 borderColor: [
//                   "rgba(255, 26, 104, 0.2)",
//                   "rgba(0, 0, 0, 0.2)"
//                 ],
//                 hoverOffset: 4
//             }]
//         },
//         options: {
//           responsive: true,
//           // maintainAspectRatio: false,
//           rotation: 270, // start angle in degrees
//           circumference: 180, // sweep angle in degrees
//           cutout: '80%',
//           borderRadius: 10,
//           aspectRatio: 2,
//           plugins: {
//             legend: {
//               display: false,
//               // position: 'top',
//             },
//             tooltip: {
//               enabled: false,
//               // position: 'top',
//             }
//           }
//         }
//     });
  
//     }
//   });
  
//   });





// $(function () {

//   var $populationChart = $("#population-chart");
//   $.ajax({
//     url: $populationChart.data("url"),
//     success: function (data) {
  
//       var ctx = $populationChart[0].getContext("2d");

//       var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
//       gradientStroke.addColorStop(0, '#80b6f4');
//       gradientStroke.addColorStop(1, '#f49080');

//       var gradientFill = ctx.createLinearGradient(500, 0, 100, 0);
//       gradientFill.addColorStop(0, "rgba(128, 182, 244, 0.6)");
//       gradientFill.addColorStop(1, "rgba(244, 144, 128, 0.6)");
  
//       new Chart(ctx, {
//         type: 'doughnut',
//         data: {
//             labels: data.labels.slice(0, 5),
//             datasets: [{
//                 data: data.data.slice(0, 5),
//                 backgroundColor: [
//                   "rgba(128, 182, 244, 0.6)",
//                   "rgba(128, 182, 244, 0.6)",
//                   "rgba(128, 182, 244, 0.6)"
//                 ],
//                 hoverOffset: 4
//             }]
//         },
//         options: {
//           rotation: 270, // start angle in degrees
//           circumference: 180, // sweep angle in degrees
//           plugins: {
//             legend: {
//               display: false,
//               // position: 'top',
//             }
//           }
//         }
//     });
  
//     }
//   });
  
//   });





//  GRADIENT BAR CHART
// $(function () {

//   var $populationChart = $("#population-chart");
//   $.ajax({
//     url: $populationChart.data("url"),
//     success: function (data) {
  
//       var ctx = $populationChart[0].getContext("2d");

//       var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
//       gradientStroke.addColorStop(0, '#80b6f4');
//       gradientStroke.addColorStop(1, '#f49080');

//       var gradientFill = ctx.createLinearGradient(500, 0, 100, 0);
//       gradientFill.addColorStop(0, "rgba(128, 182, 244, 0.6)");
//       gradientFill.addColorStop(1, "rgba(244, 144, 128, 0.6)");
  
//       new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: data.labels,
//             datasets: [{
//                 label: "Data",
//                 // borderColor: gradientStroke,
//               //   pointBorderColor: gradientStroke,
//               //   pointBackgroundColor: gradientStroke,
//               //  pointHoverBackgroundColor: gradientStroke,
//               //   pointHoverBorderColor: gradientStroke,
//                 // pointBorderWidth: 10,
//                 // pointHoverRadius: 10,
//                 // pointHoverBorderWidth: 1,
//                 // pointRadius: 3,
//                 fill: true,
//                 // radius: 0,
//                 backgroundColor: gradientFill,
//                 // borderWidth: 4,
//                 // data: data.data.slice(0, 10)
//                 data: data.data
//             }]
//         },
//         options: {
//             legend: {
//                 position: "bottom"
//             },
//             // scales: {
//             //     yAxes: [{
//             //         ticks: {
//             //             fontColor: "rgba(0,0,0,0.5)",
//             //             fontStyle: "bold",
//             //             beginAtZero: true,
//             //             maxTicksLimit: 5,
//             //             padding: 20
//             //         },
//             //         gridLines: {
//             //             drawTicks: false,
//             //             display: false
//             //         }
    
//             //     }],
//             //     xAxes: [{
//             //         gridLines: {
//             //             zeroLineColor: "transparent"
//             //         },
//             //         ticks: {
//             //             padding: 20,
//             //             fontColor: "rgba(0,0,0,0.5)",
//             //             fontStyle: "bold"
//             //         }
//             //     }]
//             // }
//         }
//     });
  
//     }
//   });
  
//   });




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




