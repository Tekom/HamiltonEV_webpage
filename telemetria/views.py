from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    data = {'test':'graph'}
    return render(request, 'telemetria/index.html', context=data)

def obtener_datos(request):
    datos = {'nombre': 'Juan', 'edad': 30}
    return JsonResponse(datos)
