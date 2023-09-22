from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sse/', views.sse, name='sse'),
    path('logout/', views.logout_view, name='logout'),
    path('download_file/<str:filename>', views.download_file, name='download_file')
]