# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from forms import *
from models import *
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings

# Permisos
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Permission, Group

def home(request):
    return render(request, 'inicio.html', {'ent': True})

# ---------------------------------------------------------
# ---------------------------------------------------------
#Grupos, checar si pertenece a grupo

def group_required(*group_names):
	def check(user):
		if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
			return True
		else:
			return False
	return user_passes_test(check, login_url='/prohibido/')

# ---------------------------------------------------------------
# Actualizar cuenta
@login_required
@transaction.atomic
def actualizar_cuenta(request):
	if request.method == 'POST':
		user_form = Usuarioform(request.POST, instance=request.user)
		if user_form.is_valid():
					user_form.save()
					messages.success(request, 'Perfil actualizado')
					print 'actualizado'
					return redirect('actualizar_cuenta')

		else:
			messages.error(request, 'Hay errores.')
	else:
		user_form = Usuarioform(instance=request.user)

	return render(request, 'editar_cuenta.html', {
        'user_form': user_form,
    })

# ---------------------------------------------------------------
# Actualizar perfil
@login_required
@transaction.atomic
def actualizar_perfil(request):
	perfil = Perfil.objects.get(pk=request.user.id)
	profile_form = Perfilform(request.POST, instance=perfil)
	if request.method == 'POST':
		profile_form = Perfilform(request.POST, instance=perfil)
		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, 'Perfil actualizado')
			print 'actualizado'
			return redirect('actualizar_perfil')

		else:
			messages.error(request, 'Hay errores.')
	else:
		profile_form = Perfilform(instance=perfil)

	return render(request, 'editar_perfil.html', {
        'profile_form': profile_form
    })


# ---------------------------------------------------------------
# Usuario subir carta , settings.VARIABLE
@login_required
def upload_carta(request):
	save = False
	form = Usuario_cartas()
	if request.method == 'POST':
		form = Usuario_cartas(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.archivo = form.cleaned_data['archivo']
            post.contenido = form.cleaned_data['contenido']
            post.email = form.cleaned_data['email']
            post.tel1 = form.cleaned_data['tel1']
            post.tel2 = form.cleaned_data['tel2']
            post.user = request.user
            post.save()
            save = True
            print save
            #return redirect('home')
	else:
            form = Usuario_cartas()
	return render(request, 'subir_carta.html', {'form': form, 'save':save})


# ---------------------------------------------------------------
# Usuario subir audio , settings.VARIABLE
@login_required
def upload_audio(request):
	save = False
	form = Usuario_audios()
	if request.method == 'POST':
		form = Usuario_audios(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.archivo = form.cleaned_data['archivo']
            post.email = form.cleaned_data['email']
            post.tel1 = form.cleaned_data['tel1']
            post.tel2 = form.cleaned_data['tel2']
            post.user = request.user
            post.save()
            save = True
            print save
            #return redirect('home')

	return render(request, 'subir_audio.html', {'form': form, 'save':save})

# ---------------------------------------------------------------
# Usuario subir video , settings.VARIABLE
@login_required
def upload_video(request):
	save = False
	form = Usuario_videos()
	if request.method == 'POST':
		form = Usuario_videos(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.archivo = form.cleaned_data['archivo']
            post.nombre = form.cleaned_data['nombre']
            post.email = form.cleaned_data['email']
            post.tel1 = form.cleaned_data['tel1']
            post.tel2 = form.cleaned_data['tel2']
            post.direccion = form.cleaned_data['direccion']
            post.formato = form.cleaned_data['formato']
            post.user = request.user
            post.save()
            save = True
            print save
            #return redirect('home')

	return render(request, 'subir_video.html', {'form': form, 'save':save})