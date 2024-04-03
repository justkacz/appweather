
// Chart.register(ChartDataLabels);

$(function () {

    var $gaugeChart = $("#city-charts3");
    $.ajax({
      url: $gaugeChart.data("url"),
      success: function (data) {
    
        var ctx = $gaugeChart[0].getContext("2d");
  
        const colors = {
          yellow: {
            default: "rgba(237, 164, 5, 1)",
            half: "rgba(237, 164, 5, 0.5)",
            quarter: "rgba(237, 164, 5, 0.25)",
            zero: "rgba(237, 164, 5, 0)"
          }
        };
  
        gradient = ctx.createLinearGradient(0, 0, 200, 0);
        gradient.addColorStop(0.15, colors.yellow.zero);
        gradient.addColorStop(0.5, colors.yellow.quarter);
        gradient.addColorStop(1, colors.yellow.half);
  
        const innerLabel = {
          id: 'innerLabel',
          afterDatasetDraw(chart, args) {
            const { ctx } = chart;
            const meta = args.meta;
            const xCoor = meta.data[0].x;
            const yCoor = meta.data[0].y;
            const perc = chart.data.datasets[0].data[0] / meta.total * 100;
            ctx.save();
            ctx.textAlign = 'center';
            ctx.font = '14px sans-serif';
            ctx.fillStyle = "rgb(245, 245, 244)";
            ctx.fillText((data.data[0].solarenergy/3.6).toFixed(1) + ' kWh/m2', xCoor, yCoor);
            ctx.restore();
          },
        };
            
        
        new Chart(ctx, {
          type: 'doughnut',
          plugins: [innerLabel, ChartDataLabels],
          data: {
              // labels: ['Score', 'Grey Area'],
              datasets: [{
                  data: [data.data[0].solarenergy/3.6, 100-data.data[0].solarenergy/3.6],
                  // data: [80, 20],
                  backgroundColor: [
                     gradient,
                    // 'rgba(0, 0, 0, 0.2)'
                    "rgba(41, 37, 36, 0.2)"
                    // "rgba(128, 182, 244, 0.6)"
                  ],
                  borderColor: [
                    "rgba(237, 164, 5, 1)",
                    "rgba(207, 206, 204, 0.3)"
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
              datalabels: {
                display: false
              },
              legend: {
                display: false,
                // position: 'top',
              },
              title: {
                display: true,
                text: 'Solarenergy',
                font: {
                  weight: 'lighter',
                  size: 13
                },
                color: "rgb(168, 162, 158)"
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
  