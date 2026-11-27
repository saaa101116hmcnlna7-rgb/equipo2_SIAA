from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Alumno, Docente, Reporte, Tutor

CLAVE = 'Clave-Segura-2026'


class PaginasPublicasTests(TestCase):
    def test_cargan(self):
        for nombre in ('index', 'bienvenida', 'login', 'registro', 'registrar_alumno',
                       'registrar_docente', 'registrar_tutor'):
            with self.subTest(nombre):
                self.assertEqual(self.client.get(reverse(nombre)).status_code, 200)


class RegistroTests(TestCase):
    def test_alumno_entra_a_su_panel(self):
        respuesta = self.client.post(reverse('registrar_alumno'), {
            'username': 'alumno1', 'password1': CLAVE, 'password2': CLAVE,
            'num_control_alumno': 'A001', 'nombre_alumno': 'Alumno Uno',
            'edad_alumno': 16, 'grado_alumno': 3, 'grupo_alumno': '306',
            'correo_alumno': 'alumno1@example.com',
        }, follow=True)
        self.assertTemplateUsed(respuesta, 'blog/panel_alumno.html')

    def test_docente_queda_pendiente(self):
        self.client.post(reverse('registrar_docente'), {
            'username': 'profe', 'password1': CLAVE, 'password2': CLAVE,
            'nombre_docente': 'Profe', 'correo_docente': 'profe@example.com',
        })
        self.assertFalse(User.objects.get(username='profe').is_active)


class PermisosTests(TestCase):
    def setUp(self):
        usuario = User.objects.create_user('profe', password=CLAVE)
        self.docente = Docente.objects.create(
            usuario=usuario, nombre_docente='Profe', correo_docente='profe@example.com')
        alumno = Alumno.objects.create(
            num_control_alumno='A001', nombre_alumno='Alumno Uno', edad_alumno=16,
            grado_alumno=3, grupo_alumno='306', correo_alumno='a1@example.com')
        self.reporte = Reporte.objects.create(
            titulo_reporte='Retardo', alumno_reporte=alumno,
            docente_reporte=self.docente, motivo_reporte='Llegó tarde')
        usuario_tutor = User.objects.create_user('tutor', password=CLAVE)
        self.tutor = Tutor.objects.create(
            usuario=usuario_tutor, nombre_tutor='Tutor', correo_tutor='t@example.com')

    def test_sin_sesion_va_al_login(self):
        respuesta = self.client.get(reverse('panel_admin'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn(reverse('login'), respuesta.url)

    def test_docente_no_entra_a_administrativo(self):
        self.client.login(username='profe', password=CLAVE)
        self.assertEqual(self.client.get(reverse('panel_admin')).status_code, 403)

    def test_tutor_solo_ve_a_sus_alumnos(self):
        self.client.login(username='tutor', password=CLAVE)
        url = reverse('reporte_detalle', args=[self.reporte.pk])
        self.assertEqual(self.client.get(url).status_code, 403)
        self.tutor.alumnos.add(self.reporte.alumno_reporte)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_paneles_cargan(self):
        User.objects.create_superuser('jefe', password=CLAVE)
        for usuario, panel in (('profe', 'panel_maestro'), ('tutor', 'panel_tutor'),
                               ('jefe', 'panel_admin')):
            with self.subTest(panel):
                self.client.login(username=usuario, password=CLAVE)
                self.assertEqual(self.client.get(reverse(panel)).status_code, 200)
