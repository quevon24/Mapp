from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone

from django.conf import settings

class Membresia(models.Model):
	nombre = models.CharField(max_length = 140)
	descripcion = models.CharField(max_length = 500)
	costo = models.FloatField()
	def __unicode__(self):
		return unicode(self.nombre)



class MembresiaUsuario(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	paquete = models.ForeignKey(Membresia)
	fecha = models.DateTimeField(default=timezone.now)
	pendiente = 1
	activo = 2
	cancelado = 3
	estado_opciones = (
	  (pendiente, 'Pendiente'),
	  (activo, 'Activo'),
	  (cancelado, 'Cancelado'),
	)
	estado = models.IntegerField(choices=estado_opciones, default=pendiente)


from pagos.models import Pago
import datetime
import time
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
##Signals
#Signal billing cycle price update Hosting
@receiver(post_save, sender=MembresiaUsuario)
def create_membresia(sender, instance, created, **kwargs):
	if created:
		now = timezone.now()
		string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
		namec = instance.user.first_name.split(' ')[0].encode('utf-8')
		payname=namec.lower() + '-'  + str(instance.user.id) +  '-'  + string
		paquete = instance.paquete.nombre
		description = 'Pago'+' '+paquete+' '+payname
		mount = instance.paquete.costo
		Pago.objects.create(descripcion=description, user=instance.user, mount=mount, content_type_id=settings.MEMBRESIA, object_id=instance.id)

		"""username = instance.user.name
		description = instance.paquete.nombre
		reference = instance.name
		pk = instance.pk
		htmlnewadmin = get_template('emailnewadminhosting.html')
		d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
		html_content = htmlnewadmin.render(d)
		msg = EmailMultiAlternatives(
			subject="Nuevo Service Hosting",
			body="Un nuevo Hospedaje Solicitado",
			from_email="Ticsup <contacto@serverticsup.com>",
			to=["Admin"+" "+"<ventas@ticsup.com>"],
			headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
		)
		msg.attach_alternative(html_content, "text/html")
		msg.send()"""
