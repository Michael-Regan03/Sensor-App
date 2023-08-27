const ctx = document.getElementById('myChart');


const fetchChartData = async() => {
    const response = await fetch(window.location.href + "chart/")
    const data = await response.json()
    console.log(data)
    return data
}

const drawChart = async() => {
    const data = await fetchChartData()
    const {chartData, chartLabels} = data
    chart = new Chart(ctx, {
        type: 'line',
        data : {
            labels: chartLabels,
            datasets: [{
                label: "% of contribution",
                data: chartData,
                boardWidth: 1
            }]
        },
        options: {
            scale: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        }
    });
}

const updateChart = async() => {
    if(chart){
        chart.destroy()
    }
    drawChart()
}

drawChart()



var graphData = {
    type: 'line',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: 'pH',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        backgroundColor: [
            'rgba(73, 198, 132, 0.5)',
        ]
      }]
    },
    options: {}
  }

const myChart = new Chart(ctx, graphData);

const socket = new WebSocket('ws://' + window.location.host + '/ws/graph/');

socket.onopen = function() {
    console.log("WebSocket connection opened");
};

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);
    var newGraphData = graphData.data.datasets[0].data;
    newGraphData.shift();
    newGraphData.push(djangoData.value);

    graphData.data.datasets[0].data = newGraphData;
    myChart.update();
    
};

socket.onclose = function(event) {
    console.log("WebSocket connection closed:", event);
};