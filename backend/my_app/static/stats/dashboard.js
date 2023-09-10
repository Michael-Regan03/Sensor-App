
const ctxTemperature = document.getElementById('temperatureChart').getContext('2d');
const ctxpHValue = document.getElementById('pHValueChart').getContext('2d');
const ctxTDSValue = document.getElementById('tdsValueChart').getContext('2d');


const socket = new WebSocket('ws://' + window.location.host + '/ws/SensorData/') //Establishing web socket connection
console.log(socket)

let chartTemperature, chartpHValue, chartTDSValue;

var chartLabels = [];

socket.onmessage = function(e) {
    const djangoData = JSON.parse(e.data);
    console.log(djangoData);

    const newPH_value = parseFloat(djangoData.pH_value); //Extracting pH value from received data
    const newTemperature = parseFloat(djangoData.temperature); //Extracting temperature from received data
    const newTDS_value = parseFloat(djangoData.tds_value); //Extracting TDS from received data
    const newTimestamp = djangoData.timestamp; //Extracting Timestamp from received data

    var newGraphDataPH = chartpHValue.data.datasets[0].data; //Updating chartpHValue with new pH_value
    var newGraphDataTemperature = chartTemperature.data.datasets[0].data; //Updating chartTemperature with the new temperature
    var newGraphDataTDS = chartTDSValue.data.datasets[0].data; //Updating chartTDSValue with the new tds_value


    newGraphDataPH.shift();
    newGraphDataTemperature.shift();
    newGraphDataTDS.shift();

    newGraphDataPH.push(newPH_value);
    newGraphDataTemperature.push(newTemperature);
    newGraphDataTDS.push(newTDS_value);


    // Update the chart's labels with the new timestamp
    var newLabels = chartpHValue.data.labels;
    newLabels.shift();
    newLabels.push(newTimestamp);


    
    // Update the chart



    chartpHValue.data.datasets[0].data = newGraphDataPH;
    chartpHValue.data.labels = newLabels;
    chartpHValue.update();

    chartTemperature.data.datasets[0].data = newGraphDataTemperature;
    chartTemperature.data.labels = newLabels;
    chartTemperature.update();

    chartTDSValue.data.datasets[0].data = newGraphDataTDS;
    chartTDSValue.data.labels = newLabels;
    chartTDSValue.update();
    
    //chartLabels.shift();
    //chartLabels.push(newTimestamp);
}


const fetchChartData = async () => {
    const response = await fetch(window.location.href + 'chart/');
    const data = await response.json();
    console.log(window.location.href + 'chart/');
    console.log(data);
    return data;
}

const drawChart = async (key, ctx) => {
    const data = await fetchChartData();
    // Access the specific chartData using the key
    const chartData = data[key]; // Assuming your data structure has keys like 'Temperature', 'pH_value', 'TDS_value'
    console.log(chartData);

    const chartLabels = data.chartLabels;   
    let chart;
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [{
                label: key,
                data: chartData,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false,
                    
                }
            }
        }
    });

    return chart;
}

const updateChart = async () => {
    if (chartTemperature) {
        chartTemperature.destroy();
    }
    if (chartpHValue) {
        chartpHValue.destroy();
    }
    if (chartTDSValue) {
        chartTDSValue.destroy();
    }
    
    chartTemperature = await drawChart('temperature_data', ctxTemperature);
    chartpHValue = await drawChart('pH_data', ctxpHValue);
    chartTDSValue = await drawChart('tds_data', ctxTDSValue);
}

updateChart();