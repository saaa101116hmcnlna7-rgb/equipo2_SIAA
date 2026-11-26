from django.shortcuts import render

def index(request):
    return render(request, 'blog/index.html')

def login_view(request):
    return render(request, 'blog/login.html')

def registro_view(request):
    return render(request, 'blog/registro.html')

def panel_alumno(request):
    return render(request, 'blog/panel_alumno.html')

def justificar_faltas(request):
    return render(request, 'blog/justificar_faltas.html')

def horario(request):
    return render(request, 'blog/horario.html')

def panel_maestro(request):
    return render(request, 'blog/panel_maestro.html')

def panel_tutor(request):
    return render(request, 'blog/panel_tutor.html')

def panel_admin(request):
    return render(request, 'blog/panel_admin.html')