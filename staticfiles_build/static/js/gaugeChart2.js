
$(function () {

    var $gaugeChart = $("#city-charts2");
    $.ajax({
      url: $gaugeChart.data("url"),
      success: function (data) {
    
        var ctx = $gaugeChart[0].getContext("2d");
  
        const colors = {
          purple: {
            default: "rgba(237, 164, 5, 1)",
            half: "rgba(237, 164, 5, 1)",
            quarter: "rgba(237, 164, 5, 0.3)",
            // zero: "rgba(237, 164, 5, 0)"
            zero: "rgba(0, 0, 0, 0)"

          },
          indigo: {
            default: "rgba(80, 102, 120, 1)",
            quarter: "rgba(80, 102, 120, 0.25)"
          }
        };
  
        gradient = ctx.createLinearGradient(0, 0, 200, 0);
        gradient.addColorStop(0.15, colors.purple.zero);
        gradient.addColorStop(0.5, colors.purple.quarter);
        // gradient.addColorStop(0.02, colors.purple.quarter);
        gradient.addColorStop(1, colors.purple.half);
  
        const innerLabel = {
          id: 'innerLabel',
          afterDatasetDraw(chart, args) {
            const { ctx } = chart;
            const meta = args.meta;
            const xCoor = meta.data[0].x;
            const yCoor = meta.data[0].y;
            ctx.save();
            ctx.textAlign = 'center';
            ctx.font = '18px sans-serif';
            ctx.fillStyle = "rgb(245, 245, 244)";
            ctx.fillText(data.data[0].windspeed + ' km/h', xCoor, yCoor);
            ctx.restore();
          },
        };
            
        
        new Chart(ctx, {
          type: 'doughnut',
          plugins: [innerLabel],
          data: {
              // labels: ['Score', 'Grey Area'],
              datasets: [{
                  data: [data.data[0].windspeed, 100-data.data[0].windspeed],
                  // data: [80, 20],
                  backgroundColor: [
                     gradient,
                    // 'rgba(0, 0, 0, 0.2)'
                    "rgba(41, 37, 36, 0.2)"
                    // "rgba(128, 182, 244, 0.6)"
                  ],
                  borderColor: [
                    // gradient,
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
                text: 'Windspeed'
              },
              tooltip: {
                enabled: false,
                // position: 'top',
              }
            }
          }
      });
    
      }
    });
    
    });
  