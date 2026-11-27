from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

class Alumno(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="alumno",
    )
    num_control_alumno = models.CharField(max_length=20, primary_key=True, unique=True)
    nombre_alumno = models.CharField(max_length=100)
    edad_alumno = models.PositiveIntegerField()
    fecha_nacimiento_alumno = models.DateField(blank=True, null=True)
    grado_alumno = models.PositiveIntegerField()
    grupo_alumno = models.CharField(max_length=10)
    turno_alumno = models.CharField(max_length=20, blank=True, null=True)
    carrera_alumno = models.CharField(max_length=50, blank=True, null=True)
    curp_alumno = models.CharField(max_length=18, unique=True, blank=True, null=True)
    correo_alumno = models.EmailField(unique=True)
    telefono_alumno = models.CharField(max_length=15, blank=True, null=True)
    direccion_alumno = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_alumno


class Docente(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="docente",
    )
    id_docente = models.AutoField(primary_key=True)
    nombre_docente = models.CharField(max_length=100)
    edad_docente = models.PositiveIntegerField(blank=True, null=True)
    curp_docente = models.CharField(max_length=18, unique=True, blank=True, null=True)
    correo_docente = models.EmailField(unique=True)
    telefono_docente = models.CharField(max_length=15, blank=True, null=True)
    materia_docente = models.CharField(max_length=50, blank=True, null=True)
    carrera_docente = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre_docente


class Administrador(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="administrador",
    )
    id_administrador = models.AutoField(primary_key=True)
    nombre_administrador = models.CharField(max_length=100)
    edad_administrador = models.PositiveIntegerField(blank=True, null=True)
    curp_administrador = models.CharField(max_length=18, unique=True, blank=True, null=True)
    correo_administrador = models.EmailField(unique=True)
    tipo_administrativo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre_administrador


class Tutor(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="tutor",
    )
    id_tutor = models.AutoField(primary_key=True)
    nombre_tutor = models.CharField(max_length=100)
    edad_tutor = models.PositiveIntegerField(blank=True, null=True)
    curp_tutor = models.CharField(max_length=18, unique=True, blank=True, null=True)
    correo_tutor = models.EmailField(unique=True)
    telefono_tutor = models.CharField(max_length=15, blank=True, null=True)
    alumnos = models.ManyToManyField(Alumno, blank=True, related_name="tutores")

    def __str__(self):
        return self.nombre_tutor


class Reporte(models.Model):
    num_reporte = models.AutoField(primary_key=True)
    titulo_reporte = models.CharField(max_length=100) # Agregué max_length porque es obligatorio en CharField
    alumno_reporte = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="reportes")
    docente_reporte = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True, related_name="reportes_creados")
    fecha_reporte = models.DateField(auto_now_add=True)
    motivo_reporte = models.TextField()
    sancion_reporte = models.TextField(blank=True, null=True)
    observaciones_reporte = models.TextField(blank=True, null=True)
    firma_orientadora_reporte = models.ImageField(upload_to="firmas/", blank=True, null=True)
    firma_alumno_reporte = models.ImageField(upload_to="firmas/", blank=True, null=True)

    def __str__(self):
        return f"Reporte #{self.num_reporte} - {self.titulo_reporte}"


class Justificante(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        APROBADO = "aprobado", "Aprobado"
        RECHAZADO = "rechazado", "Rechazado"

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="justificantes")
    fecha_falta = models.DateField()
    motivo = models.TextField()
    comprobante = models.FileField(
        upload_to="justificantes/", blank=True, null=True,
        validators=[FileExtensionValidator(["pdf", "jpg", "jpeg", "png"])],
    )
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_solicitud"]

    def __str__(self):
        return f"{self.alumno} - {self.fecha_falta} ({self.get_estado_display()})"
