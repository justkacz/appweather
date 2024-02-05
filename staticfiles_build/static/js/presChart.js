
$(function () {

  var $presChart = $("#pres-chart");
  $.ajax({
    url: $presChart.data("url"),
    success: function (data) {
  
      var ctx = $presChart[0].getContext("2d");
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
                text: 'Pressure mb'
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
          }
        }
      });
      
  
    }
  });
  
  });
