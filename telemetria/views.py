from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, HttpResponse
import mimetypes
from django.contrib.auth import logout
from threading import Thread
from django.conf import settings
import os
import time 
import json
from random import randint
import pyrebase
import pandas

config = {
            'apiKey': "AIzaSyCXoxYJ14-8THiRHs3VAM7KYNKnLEqhkMk",
            'authDomain': "hamiltonhv-database.firebaseapp.com",
            'databaseURL': "https://hamiltonhv-database-default-rtdb.firebaseio.com",
            'projectId': "hamiltonhv-database",
            'storageBucket': "hamiltonhv-database.appspot.com",
            'messagingSenderId': "1048401158234",
            'appId': "1:1048401158234:web:69af507d7af92aff357863",
            'measurementId': "G-F0E516TF2X"
        }

firebase = pyrebase.initialize_app(config)
authme = firebase.auth()
database = firebase.database()
n = 11

def home(request):
    context = {'n':range(1, n+1)}
    return render(request, 'telemetria/index.html', context)

def logout_view(request):
    context = {'n':range(1, n+1)}
    logout(request)
    
    return render(request, 'telemetria/index.html', context)

def createCSV():
    data = database.child("datos_vehiculo").get()
    data = data.val()
    df = pandas.DataFrame(data)
    df = df.transpose()
    df.to_csv('csv_files/data.csv', index=False)

def download_file(request, filename=''):
    getData(database.child("datos_vehiculo").get().val())

    if filename != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + '/csv_files/' + filename 
        path = open(filepath, 'rb')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
    
    else:
        render(request, 'telemetria/index.html')

def getData(data):
    engine_velocity = [[], []]
    car_velocity = [[], []]
    voltage = [[], []]
    current = [[], []]
    imu_x = [[], []]
    imu_y = [[], []]
    imu_z = [[], []]
    pwm = [[], []]

    graph_data = {'engine_velocity':engine_velocity,
                  'car_velocity':car_velocity,
                  'voltage':voltage,
                  'current':current,
                  'imu_x':imu_x,
                  'imu_y':imu_y,
                  'imu_z':imu_z,  
                  'pwm':pwm}

    for key in data.keys():
        for key2, value in data[key].items():
            if key2 != 'imu':
                graph_data[key2][0].append(value['value_x'])
                graph_data[key2][1].append(value['value_y'])

            else:
                graph_data['imu_x'][0].append(value['x']['value_x'])
                graph_data['imu_y'][0].append(value['y']['value_x'])
                graph_data['imu_z'][0].append(value['z']['value_x'])

                graph_data['imu_x'][1].append(value['x']['value_y'])
                graph_data['imu_y'][1].append(value['y']['value_y'])
                graph_data['imu_z'][1].append(value['z']['value_y'])


    for key in graph_data.keys():
        valores = {'eje_x':graph_data[key][0], 'eje_y':graph_data[key][1]}
        df = pandas.DataFrame(valores)
        df.to_csv(f'csv_files/{key}.csv', index=False)
    
@login_required
def sse(request):
    def event_stream():
        while True:
            last_db_item = dict(database.child('datos_vehiculo').order_by_key().limit_to_last(1).get().val()) #obtener ultimo dato en la base de datos
            last_car_data = last_db_item[list(last_db_item.keys())[0]]
           
            #Generar datos para enviar al cliente
            data = {'engine_velocity':last_car_data['engine_velocity']['value_x'],
                    'car_velocity':last_car_data['car_velocity']['value_x'],
                    'voltage':last_car_data['voltage']['value_x'],
                    'current':last_car_data['current']['value_x'],
                    'pwm':last_car_data['pwm']['value_x'],
                    'imu':{
                            'x':last_car_data['imu']['x']['value_x'],
                            'y':last_car_data['imu']['y']['value_x'],
                            'z':last_car_data['imu']['z']['value_x']
                    }
            }
            
            # Formato SSE: envía un evento "message" con los datos
            event = f"data:{json.dumps(data)}\n\n"
            
            yield event
            time.sleep(1)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    return response
