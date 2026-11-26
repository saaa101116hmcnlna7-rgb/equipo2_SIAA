from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('alumno/', views.panel_alumno, name='panel_alumno'),
    path('alumno/justificar/', views.justificar_faltas, name='justificar_faltas'),
    path('horario/', views.horario, name='horario'),
    path('maestro/', views.panel_maestro, name='panel_maestro'),
    path('tutor/', views.panel_tutor, name='panel_tutor'),
    path('administrativo/', views.panel_admin, name='panel_admin'),
]
