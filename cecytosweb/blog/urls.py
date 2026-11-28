from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('bienvenida/', views.bienvenida, name='bienvenida'),

    
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('panel/', views.panel, name='panel'),

    
    path('registro/', views.registro_view, name='registro'),
    path('registro/alumno/', views.registrar_alumno, name='registrar_alumno'),
    path('registro/docente/', views.registrar_docente, name='registrar_docente'),
    path('registro/tutor/', views.registrar_tutor, name='registrar_tutor'),

    
    path('alumno/', views.panel_alumno, name='panel_alumno'),
    path('alumno/justificar/', views.justificar_faltas, name='justificar_faltas'),
    path('horario/', views.horario, name='horario'),

    
    path('maestro/', views.panel_maestro, name='panel_maestro'),
    path('maestro/reporte/nuevo/', views.crear_reporte, name='crear_reporte'),

    
    path('tutor/', views.panel_tutor, name='panel_tutor'),


    path('administrativo/', views.panel_admin, name='panel_admin'),
    path('administrativo/docente/<int:pk>/aprobar/', views.aprobar_docente,
         name='aprobar_docente'),
    path('administrativo/justificante/<int:pk>/', views.revisar_justificante,
         name='revisar_justificante'),

    
    path('reporte/<int:pk>/', views.reporte_detalle, name='reporte_detalle'),
    path('reporte/<int:pk>/firma/<str:quien>/', views.firma_reporte, name='firma_reporte'),
    path('justificante/<int:pk>/comprobante/', views.comprobante, name='comprobante'),
]
