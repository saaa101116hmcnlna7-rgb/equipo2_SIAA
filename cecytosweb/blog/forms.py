from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Alumno, Docente, Justificante, Reporte, Tutor


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo.widget, forms.Select):
                clase = 'form-select'
            elif isinstance(campo.widget, forms.CheckboxInput):
                clase = 'form-check-input'
            else:
                clase = 'form-control'
            campo.widget.attrs['class'] = clase


class LoginForm(BootstrapMixin, AuthenticationForm):
    pass


class RegistroUsuarioForm(BootstrapMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username']


class AlumnoForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'num_control_alumno', 'nombre_alumno', 'edad_alumno', 'fecha_nacimiento_alumno',
            'grado_alumno', 'grupo_alumno', 'turno_alumno', 'carrera_alumno', 'curp_alumno',
            'correo_alumno', 'telefono_alumno', 'direccion_alumno',
        ]
        labels = {
            'num_control_alumno': 'Número de control',
            'nombre_alumno': 'Nombre completo',
            'edad_alumno': 'Edad',
            'fecha_nacimiento_alumno': 'Fecha de nacimiento',
            'grado_alumno': 'Grado (semestre)',
            'grupo_alumno': 'Grupo',
            'turno_alumno': 'Turno',
            'carrera_alumno': 'Carrera',
            'curp_alumno': 'CURP',
            'correo_alumno': 'Correo electrónico',
            'telefono_alumno': 'Teléfono',
            'direccion_alumno': 'Dirección',
        }
        widgets = {
            'fecha_nacimiento_alumno': forms.DateInput(attrs={'type': 'date'}),
            'direccion_alumno': forms.Textarea(attrs={'rows': 2}),
        }


class DocenteForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Docente
        fields = [
            'nombre_docente', 'edad_docente', 'curp_docente', 'correo_docente',
            'telefono_docente', 'materia_docente', 'carrera_docente',
        ]
        labels = {
            'nombre_docente': 'Nombre completo',
            'edad_docente': 'Edad',
            'curp_docente': 'CURP',
            'correo_docente': 'Correo electrónico',
            'telefono_docente': 'Teléfono',
            'materia_docente': 'Materia',
            'carrera_docente': 'Carrera',
        }


class TutorForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['nombre_tutor', 'edad_tutor', 'curp_tutor', 'correo_tutor', 'telefono_tutor']
        labels = {
            'nombre_tutor': 'Nombre completo',
            'edad_tutor': 'Edad',
            'curp_tutor': 'CURP',
            'correo_tutor': 'Correo electrónico',
            'telefono_tutor': 'Teléfono',
        }


class ReporteForm(BootstrapMixin, forms.ModelForm):
    
    class Meta:
        model = Reporte
        fields = [
            'titulo_reporte', 'alumno_reporte', 'motivo_reporte', 'sancion_reporte',
            'observaciones_reporte', 'firma_orientadora_reporte', 'firma_alumno_reporte',
        ]
        labels = {
            'titulo_reporte': 'Título',
            'alumno_reporte': 'Alumno',
            'motivo_reporte': 'Motivo',
            'sancion_reporte': 'Sanción',
            'observaciones_reporte': 'Observaciones',
            'firma_orientadora_reporte': 'Firma de la orientadora (imagen)',
            'firma_alumno_reporte': 'Firma del alumno (imagen)',
        }
        widgets = {
            'motivo_reporte': forms.Textarea(attrs={'rows': 3}),
            'sancion_reporte': forms.Textarea(attrs={'rows': 2}),
            'observaciones_reporte': forms.Textarea(attrs={'rows': 2}),
        }


class JustificanteForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Justificante
        fields = ['fecha_falta', 'motivo', 'comprobante']
        labels = {
            'fecha_falta': 'Fecha de la falta',
            'motivo': 'Motivo',
            'comprobante': 'Comprobante (PDF o imagen, opcional)',
        }
        widgets = {
            'fecha_falta': forms.DateInput(attrs={'type': 'date'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_fecha_falta(self):
        fecha = self.cleaned_data['fecha_falta']
        if fecha > timezone.localdate():
            raise forms.ValidationError('La fecha de la falta no puede ser futura.')
        return fecha
