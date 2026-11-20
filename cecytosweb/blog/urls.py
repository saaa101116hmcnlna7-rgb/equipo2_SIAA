from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reporte/nuevo/', views.crear_reporte, name='crear_reporte'),
    path('alumno/nuevo/', views.registrar_alumno, name='registrar_alumno'),
]