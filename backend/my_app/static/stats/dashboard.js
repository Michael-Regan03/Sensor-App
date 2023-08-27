console.log("hello")

const dashboardSlug = document.getElementById('dashboard-slug').textContent.trim()
const submitBtn = document.getElementById('submit-btn')
const dataInput = document.getElementById('data-input')
const user = document.getElementById('user').textContent.trim()
const dataBox = document.getElementById('data-box')

const socket = new WebSocket('ws://' + window.location.host + '/ws/' + dashboardSlug + "/")
console.log(socket)


socket.onmessage = function(e) {
    const{sender,message} = JSON.parse(e.data);
    
    dataBox.innerHTML += `<p>${sender}: ${message}</p>`;
    
    //
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);
    var newGraphData = chart.data.datasets[0].data;
    newGraphData.shift();
    newGraphData.push(djangoData.value);

    chart.data.datasets[0].data = newGraphData;
    chart.update();
    //
}

submitBtn.addEventListener('click', ()=> {
    const dataValue = dataInput.value
    socket.send(JSON.stringify({
        'message': dataValue
    }))
})

socket.onopen = function(e) {
}


const ctx = document.getElementById('myChart').getContext("2d");
let chart;


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
                label: "pH",
                data: chartData,
                boardWidth: 1
            }]
        },
        options: {
            scale: {
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            min: 0,  // Minimum value for y-axis
                            max: 14, // Maximum value for y-axis
                        }
                }}
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