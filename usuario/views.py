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
from django.views.generic import ListView, DeleteView, CreateView
from django.core.urlresolvers import reverse
import json

# Paginacion
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# jquery file upload
from fileupload.response import JSONResponse, response_mimetype
from fileupload.serialize import serialize

# Permisos
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Permission, Group

from paquetes.models import MembresiaUsuario

@login_required
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
# ---------------------------------------------------------------
# Usuario crear carta

@login_required
def crear_carta(request):
	nueva = Perfil_carta.objects.create(user=request.user)
	return HttpResponseRedirect(reverse('editar_carta', args=(nueva.id,)))


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Usuario subir carta , settings.VARIABLE

class PictureCreateView(CreateView):
	model = Perfil_carta_archivo
	fields = "__all__"
	#template_name = "perfil_carta_archivo_.html"

	def form_valid(self, form):
		self.object = form.save()
		files = [serialize(self.object)]
		data = {'files': files}
		response = JSONResponse(data, mimetype=response_mimetype(self.request))
		print response
		response['Content-Disposition'] = 'inline; filename=files.json'
		return response

	def form_invalid(self, form):
		data = json.dumps(form.errors)
		print data
		return HttpResponse(content=data, status=400, content_type='application/json')

@login_required
def upload_carta(request):
	save = False
	form = Usuario_cartas()
	if request.method == 'POST':
		form = Usuario_cartas(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.contenido = form.cleaned_data['contenido']
			post.email = form.cleaned_data['email']
			post.tel1 = form.cleaned_data['tel1']
			post.tel2 = form.cleaned_data['tel2']
			post.terminado = True
			post.user = request.user
			post.save()
			save = True
			print save
			#return redirect('home')
	else:
			form = Usuario_cartas()

	if 'savefile' in request.POST:
		#objs = dict(request.POST.iterlists()) #pass submit form fields in a dict
		
		#namefield = objs['name'] #get name section from form
		#namefield=namefield[0].encode('utf8') #encode to utf8 to avoid errors in latin characters
		form = Usuario_cartas(request.POST) 
		if form.is_valid():
			form.carta = 0
			form.save()

	return render(request, 'subir_carta.html', {'form': form, 'save':save}, locals())


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Usuario editar carta

def obtener_archivos_cartas(request, cartaid):
	try:
		archivos = Perfil_carta_archivo.objects.filter(carta=cartaid).values('pk' ,'user','carta','archivo')
		lista_archivos = list(archivos)
	except:
		archivos = None
		lista_archivos = list(archivos)
	else:
		response = JSONResponse(lista_archivos)
		print response
		response['Content-Disposition'] = 'inline; filename=files.json'
		return response


class PictureCreateView(CreateView):
	model = Perfil_carta_archivo
	fields = "__all__"
	#template_name = "perfil_carta_archivo_.html"

	def form_valid(self, form):
		self.object = form.save()
		files = [serialize(self.object)]
		data = {'files': files}
		response = JSONResponse(data, mimetype=response_mimetype(self.request))
		print response
		response['Content-Disposition'] = 'inline; filename=files.json'
		return response

	def form_invalid(self, form):
		data = json.dumps(form.errors)
		print data
		return HttpResponse(content=data, status=400, content_type='application/json')


class PictureDeleteView1(DeleteView):
	model = Perfil_carta_archivo

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		response = JSONResponse(True, mimetype=response_mimetype(request))
		response['Content-Disposition'] = 'inline; filename=files.json'
		return response

def borrar_archivo_carta(request, pk):
	archivo = Perfil_carta_archivo.objects.get(pk=pk)
	archivo.delete()
	print 'archivo borrado'
	response = JSONResponse(True, mimetype=response_mimetype(request))
	response['Content-Disposition'] = 'inline; filename=files.json'
	return response


@login_required
def editar_carta(request, pk):
	post = get_object_or_404(Perfil_carta, pk=pk)
	obj_id = pk 
	save = False
	form = Usuario_cartas(instance=post)
	contactform = form_agregar_contacto()
	archivos = Perfil_carta_archivo.objects.filter(user=request.user)
	num_archivos = archivos.count()
	if request.method == 'POST':
		form = Usuario_cartas(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			# post.contenido = form.cleaned_data['contenido']
			# post.email = form.cleaned_data['email']
			# post.tel1 = form.cleaned_data['tel1']
			# post.tel2 = form.cleaned_data['tel2']
			post.terminado = True
			post.user = request.user
			post.save()
			save = True
			print save
			#return redirect('home')
	else:
			form = Usuario_cartas(instance=post)
			contactform = form_agregar_contacto()

	return render(request, 'editar_carta.html', {'form': form, 'save':save, 'obj_pk':obj_id, 'archivos':archivos , 'num_archivos':num_archivos, 'contactform':contactform})


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Listar cartas

class listar_cartas(ListView):
	model = Perfil_carta
	template_name = 'lista_cartas.html'
	paginate_by = 10 # Elementos por pagina

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Pendiente'))
	def dispatch(self, *args, **kwargs):
		return super(listar_cartas, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		new_context = Perfil_carta.objects.filter(user=self.request.user.id)
		return new_context

	def get_context_data(self, **kwargs):
		context = super(ListView, self).get_context_data(**kwargs) 
		clist = Perfil_carta.objects.filter(user=self.request.user.id)
		paginator = Paginator(clist, self.paginate_by)

		page = self.request.GET.get('page')

		try:
			file = paginator.page(page)
		except PageNotAnInteger:
			file = paginator.page(1)
		except EmptyPage:
			file = paginator.page(paginator.num_pages)

		context['clist'] = file

		

		return context

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Ver a detalles carta

@login_required
@group_required('Administrador', 'Pendiente')
def carta_detalle(request, pk):
	archivos = Perfil_carta_archivo.objects.filter(carta=pk)
	carta = get_object_or_404(Perfil_carta, pk = pk)
	try:
		contacto = Contactos.objects.get(pk=carta.contacto.pk)
	except:
		contacto = None
	return render(request, 'detalles_carta.html', {'carta': carta, 'archivos':archivos, 'contacto':contacto})




# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Usuario crear audio nuevo

@login_required
def crear_audio(request):
	nueva = Perfil_audio.objects.create(user=request.user)
	return HttpResponseRedirect(reverse('editar_audio', args=(nueva.id,)))

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Usuario editar/nuevo audio

@login_required
def editar_audio(request, pk):
	post = get_object_or_404(Perfil_audio, pk=pk)
	obj_id = pk 
	save = False
	form = Usuario_audios(instance=post)
	contactform = form_agregar_contacto()
	archivos = Perfil_audio_archivo.objects.filter(user=request.user)
	num_archivos = archivos.count()
	if request.method == 'POST':
		form = Usuario_audios(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			# post.contenido = form.cleaned_data['contenido']
			# post.email = form.cleaned_data['email']
			# post.tel1 = form.cleaned_data['tel1']
			# post.tel2 = form.cleaned_data['tel2']
			post.terminado = True
			post.user = request.user
			post.save()
			save = True
			print save
			#return redirect('home')
	else:
			form = Usuario_audios(instance=post)
			contactform = form_agregar_contacto()

	return render(request, 'editar_audio.html', {'form': form, 'save':save, 'obj_pk':obj_id, 'archivos':archivos , 'num_archivos':num_archivos, 'contactform':contactform})



# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Usuario subir audio

@login_required
def upload_audio(request):
	save = False
	form = Usuario_audios()
	if request.method == 'POST':
		form = Usuario_audios(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			# post.archivo = form.cleaned_data['archivo']
			# post.email = form.cleaned_data['email']
			# post.tel1 = form.cleaned_data['tel1']
			# post.tel2 = form.cleaned_data['tel2']
			post.user = request.user
			post.terminado = True
			post.save()
			save = True
			print save
			#return redirect('home')

	return render(request, 'subir_audio.html', {'form': form, 'save':save})

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Usuario obtener archivos audio

@login_required
def obtener_archivos_audio(request, audioid):
	try:
		archivos = Perfil_audio_archivo.objects.filter(audio=audioid).values('pk' ,'user','audio','archivo')
		lista_archivos = list(archivos)
	except:
		archivos = None
		lista_archivos = list(archivos)
	else:
		response = JSONResponse(lista_archivos)
		print response
		response['Content-Disposition'] = 'inline; filename=files.json'
		return response

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Usuario borrar archivo audio

@login_required
def borrar_archivo_audio(request, pk):
	archivo = Perfil_audio_archivo.objects.get(pk=pk)
	archivo.delete()
	print 'archivo borrado'
	response = JSONResponse(True, mimetype=response_mimetype(request))
	response['Content-Disposition'] = 'inline; filename=files.json'
	return response

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Listar mensajes audio

class listar_audio(ListView):
	model = Perfil_audio
	template_name = 'lista_audio.html'
	paginate_by = 10 # Elementos por pagina

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Pendiente'))
	def dispatch(self, *args, **kwargs):
		return super(listar_audio, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		new_context = Perfil_audio.objects.filter(user=self.request.user.id)
		return new_context

	def get_context_data(self, **kwargs):
		context = super(ListView, self).get_context_data(**kwargs) 
		alist = Perfil_audio.objects.filter(user=self.request.user.id)
		paginator = Paginator(alist, self.paginate_by)

		page = self.request.GET.get('page')

		try:
			file = paginator.page(page)
		except PageNotAnInteger:
			file = paginator.page(1)
		except EmptyPage:
			file = paginator.page(paginator.num_pages)

		context['alist'] = file

		return context



# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Ver a detalles audio

@login_required
@group_required('Administrador', 'Pendiente')
def audio_detalle(request, pk):
	audio = get_object_or_404(Perfil_audio, pk = pk)
	return render(request, 'detalles_audio.html', {'audio': audio})



# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Usuario subir archivo audio

class PictureCreateView_audio(CreateView):
	model = Perfil_audio_archivo
	fields = "__all__"
	#template_name = "perfil_carta_archivo_.html"

	def form_valid(self, form):
		self.object = form.save()
		files = [serialize(self.object)]
		data = {'files': files}
		response = JSONResponse(data, mimetype=response_mimetype(self.request))
		print response
		response['Content-Disposition'] = 'inline; filename=files.json'
		return response

	def form_invalid(self, form):
		data = json.dumps(form.errors)
		print data
		return HttpResponse(content=data, status=400, content_type='application/json')


# ---------------------------------------------------------------
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
			post.terminado = True
			post.save()
			save = True
			print save
			#return redirect('home')

	return render(request, 'subir_video.html', {'form': form, 'save':save})

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Listar mensajes video

class listar_video(ListView):
	model = Perfil_video
	template_name = 'lista_video.html'
	paginate_by = 10 # Elementos por pagina

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Pendiente'))
	def dispatch(self, *args, **kwargs):
		return super(listar_video, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ListView, self).get_context_data(**kwargs) 
		vlist = Perfil_audio.objects.filter(user=self.request.user)
		paginator = Paginator(vlist, self.paginate_by)

		page = self.request.GET.get('page')

		try:
			file = paginator.page(page)
		except PageNotAnInteger:
			file = paginator.page(1)
		except EmptyPage:
			file = paginator.page(paginator.num_pages)

		context['vlist'] = file
		return context

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Ver a detalles video

@login_required
@group_required('Administrador', 'Pendiente')
def video_detalle(request, pk):
	video = get_object_or_404(Perfil_video, pk = pk)
	return render(request, 'detalles_video.html', {'video': video})

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Configuraciones usuario

@login_required
def configuraciones_usuario(request):
	usuario = User.objects.get(pk=request.user.id)
	try:
		perfil = Perfil.objects.get(user=request.user.id)
	except Perfil.DoesNotExist:
		crear_perfil = Perfil.objects.create(user=request.user)
		perfil = Perfil.objects.get(user=request.user.id)
	try:
		membresia = MembresiaUsuario.objects.get(user=usuario)
	except:
		membresia = None
	#print membresia.paquete.nombre

	return render(request, 'configuracion_usuario.html', {'usuario':usuario, 'perfil':perfil, 'membresia':membresia})

# ---------------------------------------------------------------
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
					return redirect('configuraciones_usuario')

		else:
			messages.error(request, 'Hay errores.')
	else:
		user_form = Usuarioform(instance=request.user)

	return render(request, 'editar_cuenta.html', {
		'user_form': user_form,
	})

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Actualizar perfil
@login_required
@transaction.atomic
def actualizar_perfil(request):
	perfil = Perfil.objects.get(user=request.user.id)
	profile_form = Perfilform(request.POST, instance=perfil)
	if request.method == 'POST':
		profile_form = Perfilform(request.POST, instance=perfil)
		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, 'Perfil actualizado')
			print 'actualizado'
			return redirect('configuraciones_usuario')

		else:
			messages.error(request, 'Hay errores.')
	else:
		profile_form = Perfilform(instance=perfil)

	return render(request, 'editar_perfil.html', {
		'profile_form': profile_form
	})


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Agregar contacto
@login_required
def agregar_contacto(request):
	form = form_agregar_contacto()
	if request.method == 'POST':
		form = form_agregar_contacto(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.terminado = True
			post.save()
			return redirect('lista_contactos')

	return render(request, 'agregar_contacto.html', {'form': form})

# Obtener datos contacto

@login_required
def ajax_datos_contacto(request, contactoid):
	try:
		contacto = Contactos.objects.get(pk=contactoid)
		contacto_datos = {'nombre': contacto.nombre, 'email1': contacto.email1, 'tel1': contacto.tel1, 'tel2':contacto.tel2, 'direccion':contacto.direccion}
	except:
		contacto_datos = {'nombre': 'Ninguno', 'email1': 'Ninguno', 'tel1': 'Ninguno', 'tel2':'Ninguno', 'direccion':'Ninguno'}

	response = JSONResponse(contacto_datos)
	print response
	response['Content-Disposition'] = 'inline; filename=files.json'
	return response


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Lista de contactos

class listar_contactos(ListView):
	model = Contactos
	template_name = 'lista_contactos.html'
	paginate_by = 10 # Elementos por pagina

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Pendiente'))
	def dispatch(self, *args, **kwargs):
		return super(listar_contactos, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		new_context = Contactos.objects.filter(user=self.request.user.id)
		return new_context

	def get_context_data(self, **kwargs):
		context = super(ListView, self).get_context_data(**kwargs) 
		clist = Contactos.objects.filter(user=self.request.user.id)
		print clist
		print self.request.user.id
		paginator = Paginator(clist, self.paginate_by)

		page = self.request.GET.get('page')

		try:
			file = paginator.page(page)
		except PageNotAnInteger:
			file = paginator.page(1)
		except EmptyPage:
			file = paginator.page(paginator.num_pages)

		context['clist'] = file
		return context


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Ver a detalles contacto

@login_required
@group_required('Administrador', 'Pendiente')
def contacto_detalle(request, pk):

	try:
		contacto = Contactos.objects.get(pk = pk)
		respuesta = True
	except:
		contacto = None
		respuesta = False

	return render(request, 'detalles_contacto.html', {'contacto': contacto, 'respuesta':respuesta})


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Editar contacto

@login_required
@group_required('Administrador')
def editar_contacto(request, pk):
	post = get_object_or_404(Contactos, pk=pk)
	if request.method == "POST":
			form = form_agregar_contacto(request.POST, instance=post)
			if form.is_valid():
				post = form.save(commit=False)
				post.author = request.user
				post.usuario = request.user
				post.save()
				return redirect('detalles_contacto', pk=pk)
	else:
			form = form_agregar_contacto(instance=post)
	return render(request, 'editar_contacto.html', {'form': form})

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Agregar contacto ajax
def agregar_contacto_ajax(request):

	if request.method == 'POST':
		form = form_agregar_contacto(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.terminado = True
			post.save()
		# nombre = request.POST.get('nombre')
		# print nombre
		# email1 = request.POST.get('email1')
		# print email1
		# tela = request.POST.get('tel1')
		# print tela
		# telb = request.POST.get('tel2')
		# print telb
		# direccion = request.POST.get('direccion')
		# print direccion
		# post = form_agregar_contacto(nombre=nombre, email1=email1, tel1=tela, tel2=telb, direccion=direccion, user=request.user)
		# post.save()

		contexto = {'estado':'exito', 'nombre': post.nombre}
	else:
		contexto = {'estado':'error', 'nombre':'ninguno'}

	response = JSONResponse(contexto)
	print response
	response['Content-Disposition'] = 'inline; filename=files.json'
	return response

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# Obtener contactos de usuario ajax

def obtener_contactos_ajax(request, pk):
	try:
		contactos = list(Contactos.objects.filter(user=pk).values('nombre','pk'))
	except:
		contactos = None

	response = JSONResponse(contactos)
	print response
	response['Content-Disposition'] = 'inline; filename=files.json'
	return response