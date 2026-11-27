from django.contrib import admin

from .models import Administrador, Alumno, Docente, Justificante, Reporte, Tutor


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('num_control_alumno', 'nombre_alumno', 'grado_alumno', 'grupo_alumno')
    search_fields = ('num_control_alumno', 'nombre_alumno')


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nombre_docente', 'correo_docente', 'materia_docente')
    search_fields = ('nombre_docente',)


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('nombre_tutor', 'correo_tutor')
    search_fields = ('nombre_tutor',)
    filter_horizontal = ('alumnos',)  # Aquí se asignan los alumnos a cada tutor


@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('nombre_administrador', 'correo_administrador', 'tipo_administrativo')


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('num_reporte', 'titulo_reporte', 'alumno_reporte', 'fecha_reporte')
    search_fields = ('titulo_reporte', 'alumno_reporte__nombre_alumno')


@admin.register(Justificante)
class JustificanteAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'fecha_falta', 'estado')
    list_filter = ('estado',)
