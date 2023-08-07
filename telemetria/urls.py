from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('obtener_datos/', views.obtener_datos, name='obtener_datos'),
]