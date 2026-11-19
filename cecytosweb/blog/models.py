from django.db import models

# Create your models here.

class Alumno(models.Model):
    num_control = models.CharField(max_length=20, primary_key=True, unique=True)
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    fecha_nacimiento = models.DateField(blank=True, null=True)
    grado = models.PositiveIntegerField()
    grupo = models.CharField(max_length=10)
    turno = models.CharField(max_length=20, blank=True, null=True)
    carrera = models.CharField(max_length=50, blank=True, null=True)
    curp = models.CharField(max_length=18, unique=True, blank=True, null=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.num_control})"


class Docente(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(blank=True, null=True)
    curp = models.CharField(max_length=18, unique=True, blank=True, null=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    materia = models.CharField(max_length=50, blank=True, null=True)
    carrera = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(blank=True, null=True)
    curp = models.CharField(max_length=18, unique=True, blank=True, null=True)
    correo = models.EmailField(unique=True)
    tipo_administrativo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Tutor(models.Model):
    id_tutor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(blank=True, null=True)
    curp = models.CharField(max_length=18, unique=True, blank=True, null=True)
    correo = models.EmailField(unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Reporte(models.Model):
    num_reporte = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="reportes")
    docente_reporta = models.ForeignKey( Docente, on_delete=models.SET_NULL, null=True,  blank=True, related_name="reportes_creados",)
    fecha = models.DateField(auto_now_add=True)
    motivo = models.TextField()
    sancion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    firma_orientadora = models.ImageField(upload_to="firmas/", blank=True, null=True)
    firma_alumno = models.ImageField(upload_to="firmas/", blank=True, null=True)

    def __str__(self):
        return f"Reporte #{self.num_reporte} - Alumno: {self.alumno.nombre}"