from django.urls import path,include
from . import views  # Importa las vistas de tu app

urlpatterns = [
    path('', views.index, name='index'),  # Ruta básica
]