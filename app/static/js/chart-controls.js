let chart = null;

function initChart(chartData) {
  const ctx = document.getElementById("chart").getContext("2d");

  // Enhanced chart options for better visualization
  const enhancedOptions = {
    ...chartData.options,
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: true,
        position: "top",
        labels: {
          padding: 15,
          font: {
            size: 12,
            family: "'Inter', sans-serif",
          },
        },
      },
      tooltip: {
        backgroundColor: "rgba(0, 0, 0, 0.8)",
        padding: 12,
        cornerRadius: 8,
        titleFont: {
          size: 14,
          weight: "bold",
        },
        bodyFont: {
          size: 13,
        },
      },
    },
    animation: {
      duration: 800,
      easing: "easeInOutQuart",
    },
  };

  chartData.options = enhancedOptions;
  chart = new Chart(ctx, chartData);
  updateInitialChartColors();
}

function updateChartFormat() {
  const xSelectedFormat = document.getElementById("x-axis-select").value;
  const ySelectedFormat = document.getElementById("y-axis-select").value;

  formatAxis("x", xSelectedFormat);
  formatAxis("y", ySelectedFormat);
}

function formatAxis(axis, selectedFormat) {
  const axisOptions =
    axis === "x" ? chart.options.scales.xAxes : chart.options.scales.yAxes;
  const userLanguage = window.navigator.language;

  if (!axisOptions) return;

  axisOptions.forEach(function (axisOption) {
    if (selectedFormat === "currency") {
      const currencyCode = getCurrencyCodeForLanguage(userLanguage);
      axisOption.ticks.callback = function (value) {
        return new Intl.NumberFormat(userLanguage, {
          style: "currency",
          currency: currencyCode,
        }).format(value);
      };
    } else if (selectedFormat === "percentage") {
      axisOption.ticks.callback = function (value) {
        return new Intl.NumberFormat(userLanguage, {
          style: "percent",
          minimumFractionDigits: 0,
          maximumFractionDigits: 2,
        }).format(value / 100);
      };
    } else if (selectedFormat === "length_cm") {
      axisOption.ticks.callback = function (value) {
        return value + " cm";
      };
    } else if (selectedFormat === "volume_cm3") {
      axisOption.ticks.callback = function (value) {
        return value + " cm³";
      };
    } else {
      axisOption.ticks.callback = function (value) {
        return value;
      };
    }
  });

  chart.update();
}

function getCurrencyCodeForLanguage(languageCode) {
  const currencyCodes = {
    "en-US": "USD",
    "pt-BR": "BRL",
    "es-ES": "EUR",
    "fr-FR": "EUR",
    "de-DE": "EUR",
    "ja-JP": "JPY",
    "zh-CN": "CNY",
  };

  return currencyCodes[languageCode] || "USD";
}

function updateChartType() {
  const chartType = document.getElementById("chart-type-select").value;
  const previousType = chart.config.type;
  chart.config.type = chartType;

  // Handle different chart type configurations
  if (
    chartType === "pie" ||
    chartType === "doughnut" ||
    chartType === "polarArea"
  ) {
    generateRandomColors();
    document.getElementById("bar-color-picker").disabled = true;

    // Remove axes for circular charts
    if (chart.options.scales) {
      chart.options.scales = {};
    }
  } else {
    document.getElementById("bar-color-picker").disabled = false;

    // Restore axes for other chart types
    if (
      !chart.options.scales ||
      Object.keys(chart.options.scales).length === 0
    ) {
      chart.options.scales = {
        xAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      };
    }
  }

  // Special configuration for scatter and bubble charts
  if (chartType === "scatter" || chartType === "bubble") {
    chart.data.datasets[0].showLine = false;
    chart.data.datasets[0].pointRadius = chartType === "bubble" ? 10 : 5;
    chart.data.datasets[0].pointHoverRadius = chartType === "bubble" ? 15 : 8;

    // Convert data to scatter format if needed
    if (typeof chart.data.datasets[0].data[0] !== "object") {
      const scatterData = chart.data.labels.map((label, index) => ({
        x: index,
        y: chart.data.datasets[0].data[index],
      }));
      chart.data.datasets[0].data = scatterData;
    }
  } else if (previousType === "scatter" || previousType === "bubble") {
    // Convert back from scatter format
    if (typeof chart.data.datasets[0].data[0] === "object") {
      chart.data.datasets[0].data = chart.data.datasets[0].data.map(
        (point) => point.y
      );
    }
    chart.data.datasets[0].showLine = chartType === "line";
  }

  // Special configuration for radar charts
  if (chartType === "radar") {
    chart.options.scale = {
      ticks: {
        beginAtZero: true,
      },
    };
  }

  chart.update("active");
}

function updateBarColor() {
  const barColor = document.getElementById("bar-color-picker").value;
  const chartType = chart.config.type;

  if (
    chartType === "pie" ||
    chartType === "doughnut" ||
    chartType === "polarArea"
  ) {
    // For circular charts, regenerate colors based on the selected color
    generateColorsFromBase(barColor);
  } else {
    chart.data.datasets[0].backgroundColor = barColor;
    chart.data.datasets[0].borderColor = barColor;
  }

  chart.update();
}

const availableColors = [
  "#ff5733",
  "#3498db",
  "#2ecc71",
  "#f39c12",
  "#9b59b6",
  "#e74c3c",
  "#1abc9c",
  "#34495e",
  "#ff6b6b",
  "#4ecdc4",
  "#45b7d1",
  "#f7b731",
];

function getRandomColor() {
  const randomIndex = Math.floor(Math.random() * availableColors.length);
  return availableColors[randomIndex];
}

function generateRandomColors() {
  const dataLength = chart.data.datasets[0].data.length;
  const colors = [];

  for (let i = 0; i < dataLength; i++) {
    colors.push(availableColors[i % availableColors.length]);
  }

  chart.data.datasets[0].backgroundColor = colors;
  chart.data.datasets[0].borderColor = colors.map((color) =>
    shadeColor(color, -20)
  );
  chart.data.datasets[0].borderWidth = 2;
}

function generateColorsFromBase(baseColor) {
  const dataLength = chart.data.datasets[0].data.length;
  const colors = [];

  for (let i = 0; i < dataLength; i++) {
    const shade = -40 + (i * 80) / dataLength;
    colors.push(shadeColor(baseColor, shade));
  }

  chart.data.datasets[0].backgroundColor = colors;
  chart.data.datasets[0].borderColor = colors.map((color) =>
    shadeColor(color, -20)
  );
}

function shadeColor(color, percent) {
  let R = parseInt(color.substring(1, 3), 16);
  let G = parseInt(color.substring(3, 5), 16);
  let B = parseInt(color.substring(5, 7), 16);

  R = parseInt((R * (100 + percent)) / 100);
  G = parseInt((G * (100 + percent)) / 100);
  B = parseInt((B * (100 + percent)) / 100);

  R = R < 255 ? R : 255;
  G = G < 255 ? G : 255;
  B = B < 255 ? B : 255;

  const RR = R.toString(16).length == 1 ? "0" + R.toString(16) : R.toString(16);
  const GG = G.toString(16).length == 1 ? "0" + G.toString(16) : G.toString(16);
  const BB = B.toString(16).length == 1 ? "0" + B.toString(16) : B.toString(16);

  return "#" + RR + GG + BB;
}

function updateInitialChartColors() {
  const barColor = document.getElementById("bar-color-picker").value;
  chart.data.datasets[0].backgroundColor = barColor;
  chart.data.datasets[0].borderColor = barColor;
  chart.update();
}

// Statistical chart functions
function addTrendline() {
  if (!chart || chart.data.datasets.length === 0) return;

  const data = chart.data.datasets[0].data;
  const n = data.length;

  let sumX = 0,
    sumY = 0,
    sumXY = 0,
    sumXX = 0;

  for (let i = 0; i < n; i++) {
    const y = typeof data[i] === "object" ? data[i].y : data[i];
    sumX += i;
    sumY += y;
    sumXY += i * y;
    sumXX += i * i;
  }

  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;

  const trendlineData = [];
  for (let i = 0; i < n; i++) {
    trendlineData.push(slope * i + intercept);
  }

  // Add trendline dataset
  chart.data.datasets.push({
    label: "Linha de Tendência",
    data: trendlineData,
    type: "line",
    borderColor: "#e74c3c",
    borderWidth: 2,
    borderDash: [5, 5],
    fill: false,
    pointRadius: 0,
  });

  chart.update();
}

// Enhanced print function
window.addEventListener("beforeprint", () => {
  if (chart) {
    chart.resize(600, 400);
  }
});

window.addEventListener("afterprint", () => {
  if (chart) {
    chart.resize();
  }
});
