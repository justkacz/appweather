$(function () {

    var $gaugeChart = $("#city-charts1");
    $.ajax({
      url: $gaugeChart.data("url"),
      success: function (data) {
    
        var ctx = $gaugeChart[0].getContext("2d");
  
        const colors = {
          yellow: {
            default: "rgba(237, 164, 5, 1)",
            half: "rgba(237, 164, 5, 1)",
            quarter: "rgba(237, 164, 5, 0.3)",
            zero: "rgba(0, 0, 0, 0)"

          }
        };
 
        gradient = ctx.createLinearGradient(0, 0, 200, 0);
        gradient.addColorStop(0.15, colors.yellow.zero);
        gradient.addColorStop(data.data[0].cloudcover * 0.01 * 0.8, colors.yellow.quarter);
        gradient.addColorStop(data.data[0].cloudcover * 0.01, colors.yellow.half);

  
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
            ctx.font = '20px sans-serif';
            ctx.fillStyle = "rgb(245, 245, 244)";
            ctx.fillText(data.data[0].cloudcover + '%', xCoor, yCoor);
            ctx.restore();
          },
        };
            
        
        new Chart(ctx, {
          type: 'doughnut',
          plugins: [innerLabel],
          data: {
              datasets: [{
                  data: [data.data[0].cloudcover, 100-data.data[0].cloudcover],
                  backgroundColor: [
                     gradient,
                    "rgba(41, 37, 36, 0.2)"
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
            rotation: 270,
            circumference: 180,
            cutout: '80%',
            borderRadius: 10,
            aspectRatio: 2.5,
            plugins: {
              datalabels: {
                display: false
              },
              legend: {
                display: false,
              },
              title: {
                display: true,
                text: 'Cloudcover',
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
  