from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Alumno, Docente, Administrador, Tutor, Reporte


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['num_control_alumno','nombre_alumno',
            'edad_alumno','fecha_nacimiento_alumno', 'grado_alumno', 'grupo_alumno', 'turno_alumno',
            'carrera_alumno', 'curp_alumno', 'correo_alumno', 'telefono_alumno', 'direccion_alumno',]
        widgets = {
            'fecha_nacimiento_alumno': forms.DateInput(attrs={'type': 'date'}),}


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = [ 'nombre_docente', 'edad_docente', 'curp_docente',
            'correo_docente', 'telefono_docente', 'materia_docente', 'carrera_docente',  ]




class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = [ 'nombre_tutor', 'edad_tutor', 'curp_tutor', 'correo_tutor','telefono_tutor', ]


class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = [ 'titulo_reporte','alumno_reporte','docente_reporte','motivo_reporte',
            'sancion_reporte','observaciones_reporte','firma_orientadora_reporte',
            'firma_alumno_reporte',]