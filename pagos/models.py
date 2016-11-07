from __future__ import unicode_literals

from django.db import models


from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
# Create your models here.



class Pago(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	descripcion = models.CharField(max_length = 140)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	mount = models.FloatField()
	bank = 1
	transfer = 2
	card = 3
	oxxo = 4
	payment_options = (
	  (bank, 'Deposito'),
	  (transfer, 'Trasferencia'),
	  (card, 'Tarjeta'),
	  (oxxo, 'Oxxo'),
	)
	metodo = models.IntegerField(choices=payment_options, default=bank)
	pending = 1
	verified = 2
	conflict = 3
	cancel = 4
	refund = 5
	status_options = (
	  (pending, 'Pendiente'), #en formas de pago como deposito o trasferencia, la comprobacion del pago es manual
	  (verified, 'Verificado'), #cuando la comprobacion manual se realiza por el administrador o por el sistema de forma automatica
	  (conflict, 'Conflicto'), #cuanto el pago no se pudo verificar o bien existe algun problema con el metodo de pago, tambien cuando solicitan alguna devolucion y no se concreta aun
	  (cancel, 'Cancelado'),# cuando no se deposita el pago a la cuenta ya sea trasferencia, deposito o metodo automatico
	  (refund, 'Rembolsado'), #cuando se devuelve el dinero
	)
	estado = models.IntegerField(choices=status_options, default=pending)
	fecha = models.DateTimeField(default=timezone.now)
	def __unicode__(self):
		return unicode(self.descripcion)
