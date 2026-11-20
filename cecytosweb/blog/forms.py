from django.urls import path
from . import Alumno, Docente, Administrador, Tutor, Reporte
from django.contrib.auth import models

class Alumno(models.Model):
    template_name = 'login.html'
    
    class Meta:
        model = Alumno
        fields = ['username', 'password']
        
class Docente(models.Model):
    template_name = 'login.html'
    
    class Meta:
        model = Docente
        fields = ['username', 'password']
        
class Administrador(models.Model):
    template_name = 'login.html'
    
    class Meta:
        model = Administrador
        fields = ['username', 'password']
        
class Tutor(models.Model):
    template_name = 'login.html'
    
    class Meta:
        model = Tutor
        fields = ['username', 'password']

class Reporte(models.Model):
    template_name = 'login.html'
    
    class Meta:
        model = Reporte
        fields = ['username', 'password']