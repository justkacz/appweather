$(function () {

    var $tempChart = $("#temp-chart");
    $.ajax({
      url: $tempChart.data("url"),
      success: function (data) {
        const dane = []
        const temp_max_arr = []
        const temp_min_arr = []

        for (let i = 0; i < data.data.length; i++) {
            dane.push({x: i, y: data.data[i]});
            temp_max_arr.push({x: i, y: data.temp_max[i]});
            temp_min_arr.push({x: i, y: data.temp_min[i]});
            };

        const totalDuration = 4300;
        const delayBetweenPoints = totalDuration / dane.length;
    
        var ctx = $tempChart[0].getContext("2d");
        const previousY = (ctx) => ctx.index === 0 ? ctx.chart.scales.y.getPixelForValue(100) : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y;
        const animation = {
            x: {
              easing: 'linear',
              duration: delayBetweenPoints,
              from: NaN,
              delay(ctx) {
                if (ctx.type !== 'data' || ctx.xStarted) {
                  return 0;
                }
                ctx.xStarted = true;
                return ctx.index * delayBetweenPoints;
              }
            },
            y: {
              easing: 'linear',
              duration: delayBetweenPoints,
              from: previousY,
              delay(ctx) {
                if (ctx.type !== 'data' || ctx.yStarted) {
                  return 0;
                }
                ctx.yStarted = true;
                return ctx.index * delayBetweenPoints;
              }
            }
          };

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                  label: 'Temp',
                  borderColor: "rgb(194, 120, 3)",
                  borderWidth: 2,
                  radius: 0,
                  data: dane,
                },
                {
                  label: 'Temp max',
                  fill: false,
                  borderColor: "rgb(143, 52, 0)",
                  borderDash: [5, 5],
                  borderWidth: 1,
                  radius: 0,
                  data: temp_max_arr,
                },
                {
                  label: 'Temp min',
                  fill: false,
                  borderColor: "rgb(89, 89, 88)",
                  borderDash: [5, 5],
                  borderWidth: 1,
                  radius: 0,
                  data: temp_min_arr,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                  padding: {
                    bottom: 5
                  }
                },
                title: {
                  display: true,
                  text: 'Temp Chart'
                },
                legend: {
                  position: 'right'
                },
                animation,
                interaction: {
                    intersect: false
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: function(tooltipItem) {
                                let title = data.labels[tooltipItem[0].dataIndex];
                                return title;
                            },
                            label: function(context) {
                                let label = "Temp: " + context.parsed.y
                                return label;
                            }
                        }
                    }
                },
                scales: {
                        x: {
                            type: 'linear',
                            title: {
                              display: true,
                              text: 'Capitals'
                            },
                            ticks: {                
                                callback: (index) => data.labels[index],
                                stepSize: 1,
                                // autoSkip: false,      
                                fontSize: 7 
                            }
                        },
                        y: {
                          title: {
                            display: true,
                            text: 'Temperature C'
                          }
                        }
                      }
            }
            });
    
      }
    });
    
    });
