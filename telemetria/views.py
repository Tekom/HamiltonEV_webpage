from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
import time 
import json
from random import randint

def home(request):
    data = {'test':'graph'}
    return render(request, 'telemetria/index.html', context=data)

@csrf_exempt
def sse(request):
    def event_stream():
        cont = 0
        while cont == 0:
            # Generar datos para enviar al cliente
            data = {'engine_velocity':randint(-20, 20),
                    'car_velocity':randint(-20, 20),
                    'voltage':randint(-20, 20),
                    'current':randint(-20, 20),
                    'imu':randint(-20, 20),
                    'pwm':randint(-20, 20)}
            
            # Formato SSE: envía un evento "message" con los datos
            event = f"data:{json.dumps(data)}\n\n"
            
            cont+=1
            time.sleep(1)
            yield event
              # Simula una pausa de 1 segundo entre eventos

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    return response
