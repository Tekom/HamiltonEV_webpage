const engine_velocity = document.getElementById('myChart');
const car_velocity = document.getElementById('velocity');
const voltage = document.getElementById('voltage');
const current = document.getElementById('current');
const imu = document.getElementById('imu');
const pwm = document.getElementById('pwm');


var opciones = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      grid: {
        display: false
      },
      title: {
        display: true,
        text: 'Tiempo [s]', // Nombre del eje X
        font: {
          weight: 'bold'
        }
      }
    },
    y: {
      grid: {
        display: true
      },
      title: {
        display: true,
        text: '', // Nombre del eje Y
        font: {
          weight: 'bold'
        }
      }
    }
  }
};

var opciones_copia = {};

var graph_data = {
    type: 'line',
    data: {
      labels: ['jan', 'feb', 'mar', 'apr', 'may', 'jun'],
      datasets: [{
        label: '',
        data: [0, 0, 0, 0, 0, 0],
      }]
    },
    options: opciones
};

var graph_data_engine = JSON.parse(JSON.stringify(graph_data));;
var graph_data_velocity = JSON.parse(JSON.stringify(graph_data));;
var graph_data_voltage = JSON.parse(JSON.stringify(graph_data));;
var graph_data_current = JSON.parse(JSON.stringify(graph_data));;
var graph_data_imu = JSON.parse(JSON.stringify(graph_data));;
var graph_data_pwm = JSON.parse(JSON.stringify(graph_data));;

var engine_chart = new Chart(engine_velocity, graph_data_engine);
var velocity_chart = new Chart(car_velocity, graph_data_velocity);
var voltage_chart = new Chart(voltage, graph_data_voltage);
var current_chart = new Chart(current, graph_data_current);
var imu_chart = new Chart(imu, graph_data_imu);
var pwm_chart = new Chart(pwm, graph_data_pwm);

const cloud_data = {'engine_velocity':{
  'title': 'Velocidad motor [rad/s]',
  'y_label': 'RPM [rad]',
  'variable': graph_data_engine,
},
'car_velocity':{
  'title': 'Velocidad automovil [km/h]',
  'y_label': 'Velocidad [km]',
  'variable': graph_data_velocity,
},
'voltage':{
  'title': 'Voltaje motor [V]',
  'y_label': 'Voltaje [V]',
  'variable': graph_data_voltage,
},
'current':{
  'title': 'Corriente motor [A]',
  'y_label': 'Corriente [A]',
  'variable': graph_data_current,
},
'imu':{
  'title': 'Giroscopio',
  'y_label': 'Grados [°]',
  'variable': graph_data_imu,
},
'pwm':{
  'title': 'PWM',
  'y_label': 'Amplitud [V]',
  'variable': graph_data_pwm,
}}

var socket = new WebSocket('ws://' + "https://hamiltonev.azurewebsites.net" + '/ws/telemetria/');

socket.onmessage = function(e) {
    var djangoData = JSON.parse(e.data);
    var keys = Object.keys(djangoData);
    
    for (let i = 0; i < keys.length; i++) {
      var new_graph_data = cloud_data[keys[i]].variable.data.datasets[0].data;
      new_graph_data.shift();
      new_graph_data.push(djangoData[keys[i]]);
      cloud_data[keys[i]].variable.data.datasets[0].data = new_graph_data;

      cloud_data[keys[i]].variable.options.scales.y.title.text = cloud_data[keys[i]].y_label;
      cloud_data[keys[i]].variable.data.datasets[0].label = cloud_data[keys[i]].title;
    }

    engine_chart.update();
    velocity_chart.update();
    voltage_chart.update();
    current_chart.update();
    imu_chart.update();
    pwm_chart.update();
}