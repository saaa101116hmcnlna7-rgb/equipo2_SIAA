from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Alumno, Docente, Administrador, Tutor, Reporte


class AlumnoListView(ListView):
    model = Alumno
    template_name = 'alumnos/lista.html'
    context_object_name = 'alumnos'

class AlumnoCreateView(CreateView):
    model = Alumno
    fields = '__all__'
    template_name = 'alumnos/formulario.html'
    success_url = reverse_lazy('alumno_lista')

class AlumnoUpdateView(UpdateView):
    model = Alumno
    fields = '__all__'
    template_name = 'alumnos/formulario.html'
    success_url = reverse_lazy('alumno_lista')

class AlumnoDeleteView(DeleteView):
    model = Alumno
    template_name = 'alumnos/confirmar_eliminar.html'
    success_url = reverse_lazy('alumno_lista')



class DocenteListView(ListView):
    model = Docente
    template_name = 'docentes/lista.html'
    context_object_name = 'docentes'

class DocenteCreateView(CreateView):
    model = Docente
    fields = '__all__'
    template_name = 'docentes/formulario.html'
    success_url = reverse_lazy('docente_lista')

class DocenteUpdateView(UpdateView):
    model = Docente
    fields = '__all__'
    template_name = 'docentes/formulario.html'
    success_url = reverse_lazy('docente_lista')

class DocenteDeleteView(DeleteView):
    model = Docente
    template_name = 'docentes/confirmar_eliminar.html'
    success_url = reverse_lazy('docente_lista')


class AdministradorListView(ListView):
    model = Administrador
    template_name = 'administradores/lista.html'
    context_object_name = 'administradores'

class AdministradorCreateView(CreateView):
    model = Administrador
    fields = '__all__'
    template_name = 'administradores/formulario.html'
    success_url = reverse_lazy('administrador_lista')

class AdministradorUpdateView(UpdateView):
    model = Administrador
    fields = '__all__'
    template_name = 'administradores/formulario.html'
    success_url = reverse_lazy('administrador_lista')

class AdministradorDeleteView(DeleteView):
    model = Administrador
    template_name = 'administradores/confirmar_eliminar.html'
    success_url = reverse_lazy('administrador_lista')



class TutorListView(ListView):
    model = Tutor
    template_name = 'tutores/lista.html'
    context_object_name = 'tutores'

class TutorCreateView(CreateView):
    model = Tutor
    fields = '__all__'
    template_name = 'tutores/formulario.html'
    success_url = reverse_lazy('tutor_lista')

class TutorUpdateView(UpdateView):
    model = Tutor
    fields = '__all__'
    template_name = 'tutores/formulario.html'
    success_url = reverse_lazy('tutor_lista')

class TutorDeleteView(DeleteView):
    model = Tutor
    template_name = 'tutores/confirmar_eliminar.html'
    success_url = reverse_lazy('tutor_lista')


class ReporteListView(ListView):
    model = Reporte
    template_name = 'reportes/lista.html'
    context_object_name = 'reportes'

class ReporteDetailView(DetailView):
    model = Reporte
    template_name = 'reportes/detalle.html'
    context_object_name = 'reporte'

class ReporteCreateView(CreateView):
    model = Reporte
    fields = '__all__'
    template_name = 'reportes/formulario.html'
    success_url = reverse_lazy('reporte_lista')

class ReporteUpdateView(UpdateView):
    model = Reporte
    fields = '__all__'
    template_name = 'reportes/formulario.html'
    success_url = reverse_lazy('reporte_lista')

class ReporteDeleteView(DeleteView):
    model = Reporte
    template_name = 'reportes/confirmar_eliminar.html'
    success_url = reverse_lazy('reporte_lista')
