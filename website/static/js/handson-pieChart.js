(function () {
  const handson_PieChart = document.getElementById("handsonPieChart");

  Chart.register(ChartDataLabels);

  const data = {
    labels: ["Passed Applicants", "Failed Applicants"],
    datasets: [
      {
        label: "My First Dataset",
        data: [5, 5],
        backgroundColor: ["#18a843", "#990e23"],
        hoverOffset: 2,
      },
    ],
  };

  const config = {
    type: "pie",
    data: data,
    options: {
      plugins: {
        tooltip: {
          enabled: false,
        },
        datalabels: {
          formatter: (value, ctx) => {
            const datapoints = ctx.chart.data.datasets[0].data;
            const total = datapoints.reduce(
              (total, datapoint) => total + datapoint,
              0
            );
            const percentage = ((value / total) * 100).toFixed(2) + "%";
            return percentage;
          },
          color: "#fff",
          font: {
            weight: "bold",
            size: 12,
          },
        },
      },
    },
  };

  new Chart(handson_PieChart, config);
})();
