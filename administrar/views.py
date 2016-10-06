from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext
from forms import *

#Permisos
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

#Registrar
from django.contrib.auth.models import User, Permission, Group

# Importar modelos de app usuario
from usuario.models import Perfil, Activar_cuenta


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
# Error 404

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
# Error 500

def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Grupos, checar si pertenece a grupo

def group_required(*group_names):
    def check(user):
        if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
            return True
        else:
            return False
    return user_passes_test(check, login_url='/prohibido/')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
# Acceso prohibido si no pertenece a grupo

@login_required
def prohibido(request):
    current_user = request.user
    us = post = get_object_or_404(User, username=current_user)
    return render(request, '403.html', {'user':us})


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
# Registrarse

def registrar(request):
        context = RequestContext(request)
        registered = False
        if request.method == 'POST':
                uform = Registrar(data = request.POST)
                if uform.is_valid():
                        user = uform.save()
                        # form brings back a plain text string, not an encrypted password
                        pw = user.password
                        # thus we need to use set password to encrypt the password string
                        user.set_password(pw)
                        user.save()
                        registered = True
                else:
                        print uform.errors
        else:
                uform = Registrar()

        return render_to_response('registrar.html', {'uform': uform, 'registered': registered }, context)



# ---------------------------------------------------------------
# Activar cuenta, verificar email

def activarcuenta(request, codigo, email):
    try:
        activar = Activar_cuenta.objects.get(clave=codigo, email=email)
        try:
            usuario = Perfil.objects.get(user=activar.user)
        except Perfil.DoesNotExist:
            activar = None
            usuario = None
            exito = False
    except Activar_cuenta.DoesNotExist:
        activar = None
        usuario = None
        exito = False

    
    else:
		usuario.email_verif =True
		activar.uso = True
		usuario.save()
		activar.save()
		try:
			g = Group.objects.get(name='Pendiente')
		except Group.DoesNotExist:
			g = None
		else:
			g.user_set.add(usuario)
		exito = True

    return render(request, 'activacion.html', {'usuario': usuario, 'activar':activar, 'exito':exito})