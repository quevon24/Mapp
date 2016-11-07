from django.shortcuts import render

# Create your views here.

from paquetes.models import Membresia, MembresiaUsuario

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
import json


from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from pagos.models import Pago
#content TypeError

from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType

import conekta
conekta.api_key = 'key_zkkg2WvCCoBdbiQq'

@csrf_protect
@login_required
def ver_paquetes(request):
	#idpackage = request.session['idpackage']
	try:
		paquetes = Membresia.objects.filter()
	except:
		paquetes = None
	current_user = request.user
	#function redirect if Customer Does not exist
	date = timezone.now()
	#print dat
	if request.method == 'POST':
		idpackage=request.POST['paquete']
		paquete = Membresia.objects.get(id=idpackage)
		#status = Status.objects.get(name='Pendiente')
		membresiauser,created = MembresiaUsuario.objects.get_or_create(user=current_user, paquete=paquete)
		if created:
			membresiauser.save()
		return HttpResponseRedirect(reverse('pagopaquete', args=(membresiauser.id,)))	

	return render(request, 'paquetes_disponibles.html', {'paquetes': paquetes,})


from django.conf import settings

@login_required
def pagopaquete(request, paquete):
	current_user = request.user
	membresia = MembresiaUsuario.objects.get(id=paquete)
	paquete = membresia.paquete
	payment = get_object_or_404(Pago, content_type_id=settings.MEMBRESIA, object_id = membresia.pk, user=current_user)
	#method = Method.objects.get(pk = 1)
	now = timezone.now()
	string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
	namec = membresia.user.first_name.split(' ')[0].encode('utf-8')
	payname=namec.lower() + '-'  + str(membresia.user.id) +  '-'  + string
	print payname
	invoice = str(payment.id)+'-'+string
	#PayPalPaymentsForm
	
	if request.POST:
		print request.POST
		if 'paymentcard' in request.POST:
			print "card"
			try:
				mount = int(payment.mount)*100
				charge = conekta.Charge.create({
					"amount": mount,
					"currency": "MXN",
					"description": payment.id,
					"reference_id": payname,
					"card": request.POST["conektaTokenId"] #Para cargo con tarjeta
					#request.form["conektaTokenId"], request.params["conektaTokenId"], "tok_a4Ff0dD2xYZZq82d9"
				})
				print charge.status
				print charge.fee
				print charge.paid_at
				if charge.status=='paid':
					paymentcard = get_object_or_404(Pago, pk = payment.pk, user=current_user)
					paymentcard.metodo=3
					paymentcard.estado=2
					paymentcard.fecha=timezone.now()
					paymentcard.save()
					#messages.add_message(request, messages.SUCCESS, 'Pago realizado con exito!', extra_tags='alert alert-success alert-dismissable')
					return HttpResponseRedirect(reverse('configuraciones_usuario'))
					#newpay.save() #cuando se usa objects.create se salva en automatico el modelo no es necesario salvarlo
			except conekta.ConektaError as e:
				#messages.add_message(request, messages.ERROR, 'El pago no puedo ser procesado, intente de nuevo por favor.', extra_tags='alert alert-danger alert-dismissable')
				print e.message
				#el pago no pudo ser procesado

		elif 'paymentcash' in request.POST:
			now = timezone.now()
			expire = now + timedelta(days = 10)
			month = '%02d' % expire.month
			day = '%02d' % expire.day
			date = str(expire.year)+'-'+str(month)+'-'+str(day)
			expire = str(day)+'/'+str(month)+'/'+str(expire.year)
			print date
			print "oxxo pago"
			try:
				mount = int(payment.mount)*100
				charge = conekta.Charge.create({
					"amount": mount,
					"currency": "MXN",
					"description": payment.id,
					"reference_id": payname,
					"cash": { #para cargo en oxxo
					    "type": "oxxo",
					    "expires_at": date
					  },
				})
				print charge.status
				print charge.fee
				print charge.paid_at
				print charge.payment_method["barcode_url"] #Para cargo en Oxxo
				request.session['oxxourl'] = charge.payment_method["barcode_url"]
				request.session['oxxocode'] = charge.payment_method["barcode"]
				request.session['mount'] = payment.mount
				request.session['reference'] = payment.id
				request.session['expire'] = expire
				return HttpResponseRedirect('/pago/oxxo')
			except conekta.ConektaError as e:
				print e.messag

	return render(request, 'pago_paquete.html', {'paquete': paquete,'membresia':membresia})



def oxxohtml(request):
	oxxocode = request.session['oxxocode']
	oxxourl = request.session['oxxourl']
	mount = request.session['mount']
	reference = request.session['reference']
	expire = request.session['expire']

	return render(request, 'oxxo.html', {'oxxocode': oxxocode,'oxxourl':oxxourl, 'mount':mount,'reference':reference,'expire':expire})




