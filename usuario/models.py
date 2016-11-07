# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import time
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError
from smart_selects.db_fields import ChainedForeignKey 


#generar clave activacion
import uuid

#Correo
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User, Permission, Group

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'user_{0}/{1}'.format(instance.user.id, filename)

def user_directoryfile_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'user_{0}/files/{1}'.format(instance.user.id, filename)


class Contactos(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateTimeField(default=timezone.now)
	nombre = models.CharField(max_length=100, null=True, blank=True)
	email1 = models.EmailField(null=True, blank=True)
	tel1 = models.CharField(max_length=40)
	tel2 = models.CharField(max_length=40)
	direccion = models.CharField(max_length=200)

	def __unicode__(self):
		return '%s' % (self.nombre)

class Perfil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	edad = models.IntegerField(blank=True, null=True)
	telefono = models.CharField(max_length=15, blank=True, null=True)
	celular = models.CharField(max_length=15, blank=True, null=True)
	sexo_options = (
		(1, 'Hombre'),
		(2, 'Mujer'),
		)
	sexo = models.IntegerField(choices=sexo_options, blank=True, null=True)
	direccion = models.TextField(max_length=100, blank=True, null=True)
	descripcion = models.TextField(max_length=200, blank=True, null=True)
	email_verif = models.BooleanField(default=False)
	primera_visita = models.BooleanField(default=True)

	def __unicode__(self):
		return '%s' % (self.user)

	class Meta:
		verbose_name_plural = "Perfiles"

def validar_carta(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.pdf','.doc','.docx','.jpg']
  if not ext in valid_extensions:
	raise ValidationError(u'Archivo no soportado!')
	
class Perfil_carta(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateTimeField(default=timezone.now)
	contenido = models.TextField(max_length=1000, blank=True, null=True)
	contacto = models.ForeignKey(Contactos, blank=True, null=True )
	terminado = models.BooleanField(default=False) # poner true cuando se guarda

	def __unicode__(self):
		return '%s - %s' % (self.user, self.fecha)

	class Meta:
		verbose_name_plural = "Cartas"

class Perfil_carta_archivo(models.Model):
	user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True,)
	carta = models.ForeignKey(Perfil_carta, blank=True, null=True)
	slug = models.SlugField(max_length=500, blank=True, null=True)
	archivo = models.FileField(upload_to = user_directoryfile_path, null=True, blank=True)

	def __unicode__(self):
		return self.archivo.name

	@models.permalink
	def get_absolute_url(self):
		return ('editar_carta', )

	def save(self, *args, **kwargs):
		self.slug = self.archivo.name
		super(Perfil_carta_archivo, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		#"""delete -- Remove to leave file."""
		self.archivo.delete(False)
		super(Perfil_carta_archivo, self).delete(*args, **kwargs)



def validar_audio(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.wav','.mp3','.mp4']
  if not ext in valid_extensions:
	raise ValidationError(u'Archivo no soportado!')

class Perfil_audio(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateTimeField(default=timezone.now)
	archivo = models.FileField(upload_to = user_directoryfile_path, null=True, blank=True, validators=[validar_audio])
	email = models.EmailField(null=True, blank=True)
	tel1 = models.CharField(max_length=40)
	tel2 = models.CharField(max_length=40)
	terminado = models.BooleanField(default=False) # poner true cuando se guarda

	def __unicode__(self):
		return '%s - %s' % (self.user, self.fecha)

	class Meta:
		verbose_name_plural = "Audios"

def validar_video(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.3gp','.avi','.mp4']
  if not ext in valid_extensions:
	raise ValidationError(u'Archivo no soportado!')

class Perfil_video(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateTimeField(default=timezone.now)
	archivo = models.FileField(upload_to = user_directoryfile_path, null=True, blank=True, validators=[validar_video])
	nombre = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	tel1 = models.CharField(max_length=40)
	tel2 = models.CharField(max_length=40)
	direccion = models.CharField(max_length=200)
	formato_options = (
		(1, 'Digital'),
		(2, 'USB'),
		(3, 'CD'),
		(4, 'DVD'),
		)
	formato = models.IntegerField(choices=formato_options, blank=True, null=True)
	terminado = models.BooleanField(default=False) # poner true cuando se guarda

	def __unicode__(self):
		return '%s - %s' % (self.user, self.fecha)

	class Meta:
		verbose_name_plural = "Videos"

class Activar_cuenta(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	clave = models.CharField(max_length=40, null=True, blank=True)
	uso = models.BooleanField(default=False)
	email = models.EmailField(null=True, blank=True)

class conteo_mensajes(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	carta = models.IntegerField(default=0)
	audio = models.IntegerField(default=0)
	video = models.IntegerField(default=0)
	carta_extra = models.IntegerField(default=0)
	audio_extra = models.IntegerField(default=0)
	video_extra = models.IntegerField(default=0)


# ------------------------------------------------------
# Crear perfil cuando se crea usuario y enviar email de verificacion
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
	if created:
		Perfil.objects.create(user=instance)
		activacionrandom = str(uuid.uuid4())
		activacionrandom = activacionrandom.replace("-","")
		activacionrandom = activacionrandom[0:30]
		Activar_cuenta.objects.create(user=instance, clave=activacionrandom, email=instance.email)
		subject = 'Verificar email'
		from_email = settings.EMAIL_SALIDA
		to_email = [instance.email]
		message_email = "Verifica tu email! Da clic en el siguiente enlace: \ http://3ce476da.ngrok.io/usuario/activar/%s/%s" % (activacionrandom, instance.email)
		send_mail(subject, message_email, from_email, to_email, fail_silently=True)