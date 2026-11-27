from pathlib import Path

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (AlumnoForm, DocenteForm, JustificanteForm, RegistroUsuarioForm,
                    ReporteForm, TutorForm)
from .models import Alumno, Docente, Justificante, Reporte
from .roles import requiere_rol, rol_de

PANELES = {
    'admin': 'panel_admin',
    'docente': 'panel_maestro',
    'tutor': 'panel_tutor',
    'alumno': 'panel_alumno',
}


# ---------- Páginas generales ----------

def index(request):
    return render(request, 'blog/index.html')


def bienvenida(request):
    return render(request, 'blog/bienvenida.html')


@login_required
def panel(request):
    """Envía a cada usuario a su panel según su rol."""
    destino = PANELES.get(rol_de(request.user))
    if destino:
        return redirect(destino)
    messages.warning(request, 'Tu cuenta no tiene un perfil asignado.')
    return redirect('index')


@login_required
def horario(request):
    return render(request, 'blog/horario.html')


# ---------- Registro ----------

def registro_view(request):
    return render(request, 'inicio_secion/tipo_usuario.html')


def _registrar(request, clase_form, plantilla, campo_correo, requiere_aprobacion=False):
    datos = request.POST if request.method == 'POST' else None
    usuario_form = RegistroUsuarioForm(datos)
    perfil_form = clase_form(datos)

    if request.method == 'POST':
        # Se validan los dos para mostrar todos los errores a la vez.
        validos = [usuario_form.is_valid(), perfil_form.is_valid()]
        if all(validos):
            with transaction.atomic():
                usuario = usuario_form.save(commit=False)
                usuario.email = perfil_form.cleaned_data[campo_correo]
                usuario.is_active = not requiere_aprobacion
                usuario.save()
                perfil = perfil_form.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

            if requiere_aprobacion:
                messages.info(request, 'Cuenta creada. Un administrador debe aprobarla '
                                       'antes de que puedas iniciar sesión.')
                return redirect('login')

            login(request, usuario)
            messages.success(request, 'Tu cuenta se creó correctamente.')
            return redirect('panel')

    return render(request, plantilla, {'usuario_form': usuario_form, 'perfil_form': perfil_form})


def registrar_alumno(request):
    return _registrar(request, AlumnoForm, 'inicio_secion/nuevo_alumno.html', 'correo_alumno')


def registrar_docente(request):
    return _registrar(request, DocenteForm, 'inicio_secion/nuevo_docente.html',
                      'correo_docente', requiere_aprobacion=True)


def registrar_tutor(request):
    return _registrar(request, TutorForm, 'inicio_secion/nuevo_tutor.html', 'correo_tutor')


# ---------- Alumno ----------

@requiere_rol('alumno')
def panel_alumno(request):
    alumno = request.user.alumno
    return render(request, 'blog/panel_alumno.html', {
        'alumno': alumno,
        'reportes': alumno.reportes.select_related('docente_reporte').order_by('-num_reporte'),
        'justificantes': alumno.justificantes.all(),
    })


@requiere_rol('alumno')
def justificar_faltas(request):
    if request.method == 'POST':
        form = JustificanteForm(request.POST, request.FILES)
        if form.is_valid():
            justificante = form.save(commit=False)
            justificante.alumno = request.user.alumno
            justificante.save()
            messages.success(request, 'Tu justificante se envió para revisión.')
            return redirect('panel_alumno')
    else:
        form = JustificanteForm()
    return render(request, 'blog/justificar_faltas.html', {'form': form})


# ---------- Docente ----------

@requiere_rol('docente')
def panel_maestro(request):
    docente = request.user.docente
    return render(request, 'blog/panel_maestro.html', {
        'docente': docente,
        'reportes': docente.reportes_creados.select_related('alumno_reporte').order_by('-num_reporte'),
    })


@requiere_rol('docente')
def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.docente_reporte = request.user.docente
            reporte.save()
            messages.success(request, 'Reporte guardado.')
            return redirect('reporte_detalle', pk=reporte.pk)
    else:
        form = ReporteForm()
    return render(request, 'blog/crear_reporte.html', {'form': form})


# ---------- Tutor ----------

@requiere_rol('tutor')
def panel_tutor(request):
    tutor = request.user.tutor
    return render(request, 'blog/panel_tutor.html', {
        'tutor': tutor,
        'alumnos': tutor.alumnos.prefetch_related('reportes__docente_reporte', 'justificantes'),
    })


# ---------- Administrativo ----------

@requiere_rol('admin')
def panel_admin(request):
    return render(request, 'blog/panel_admin.html', {
        'total_alumnos': Alumno.objects.count(),
        'total_docentes': Docente.objects.count(),
        'total_reportes': Reporte.objects.count(),
        'docentes_pendientes': Docente.objects.filter(usuario__is_active=False),
        'justificantes': Justificante.objects.filter(
            estado=Justificante.Estado.PENDIENTE).select_related('alumno'),
        'reportes': Reporte.objects.select_related(
            'alumno_reporte', 'docente_reporte').order_by('-num_reporte')[:20],
    })


@requiere_rol('admin')
@require_POST
def aprobar_docente(request, pk):
    docente = get_object_or_404(Docente, pk=pk, usuario__is_active=False)
    docente.usuario.is_active = True
    docente.usuario.save(update_fields=['is_active'])
    messages.success(request, f'Se aprobó la cuenta de {docente}.')
    return redirect('panel_admin')


@requiere_rol('admin')
@require_POST
def revisar_justificante(request, pk):
    justificante = get_object_or_404(Justificante, pk=pk)
    decision = request.POST.get('decision')
    if decision in (Justificante.Estado.APROBADO, Justificante.Estado.RECHAZADO):
        justificante.estado = decision
        justificante.save(update_fields=['estado'])
        messages.success(request, 'Justificante actualizado.')
    return redirect('panel_admin')


# ---------- Consulta de reportes y archivos ----------

def _puede_ver_reporte(user, reporte):
    rol = rol_de(user)
    if rol == 'admin':
        return True
    if rol == 'docente':
        return reporte.docente_reporte_id == user.docente.pk
    if rol == 'alumno':
        return reporte.alumno_reporte_id == user.alumno.pk
    if rol == 'tutor':
        return user.tutor.alumnos.filter(pk=reporte.alumno_reporte_id).exists()
    return False


def _obtener_reporte(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)
    if not _puede_ver_reporte(request.user, reporte):
        raise PermissionDenied
    return reporte


def _enviar_archivo(archivo, descargar=False):
    if not archivo:
        raise Http404('No hay archivo.')
    try:
        contenido = archivo.open('rb')
    except FileNotFoundError:
        raise Http404('El archivo no existe.')
    return FileResponse(contenido, as_attachment=descargar, filename=Path(archivo.name).name)


@login_required
def reporte_detalle(request, pk):
    return render(request, 'blog/reporte_detalle.html', {'reporte': _obtener_reporte(request, pk)})


@login_required
def firma_reporte(request, pk, quien):
    reporte = _obtener_reporte(request, pk)
    firmas = {
        'orientadora': reporte.firma_orientadora_reporte,
        'alumno': reporte.firma_alumno_reporte,
    }
    return _enviar_archivo(firmas.get(quien))


@login_required
def comprobante(request, pk):
    justificante = get_object_or_404(Justificante, pk=pk)
    rol = rol_de(request.user)
    permitido = (
        rol == 'admin'
        or (rol == 'alumno' and justificante.alumno_id == request.user.alumno.pk)
        or (rol == 'tutor'
            and request.user.tutor.alumnos.filter(pk=justificante.alumno_id).exists())
    )
    if not permitido:
        raise PermissionDenied
    return _enviar_archivo(justificante.comprobante, descargar=True)
