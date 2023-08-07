from django.shortcuts import render

def home(request):
    data = {'test':'graph'}
    return render(request, 'telemetria/index.html', context=data)
