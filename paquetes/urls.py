from django.conf.urls import url, include
from paquetes import views

urlpatterns = [
   url(r'^paquetes/$', views.ver_paquetes, name='ver_paquetes'),
   url(r'^pago_paquete/(?P<paquete>\w+)/$', views.pagopaquete, name='pagopaquete'),
   url(r'^pago/oxxo/$', views.oxxohtml, name='oxxohtml'),
]