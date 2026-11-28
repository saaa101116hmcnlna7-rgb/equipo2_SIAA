from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def rol_de(user):
    if not user.is_authenticated:
        return None
    if user.is_staff or hasattr(user, 'administrador'):
        return 'admin'
    for rol in ('docente', 'tutor', 'alumno'):
        if hasattr(user, rol):
            return rol
    return None


def requiere_rol(rol):
    
    def decorador(vista):
        @wraps(vista)
        @login_required
        def envoltura(request, *args, **kwargs):
            if rol_de(request.user) != rol:
                raise PermissionDenied
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador


def contexto_rol(request):
    return {'rol': rol_de(request.user)}
