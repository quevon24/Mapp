from django.conf.urls import url, include
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete, password_change, password_change_done

import administrar.views
from usuario import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    #url(r'^usuario/modificar_perfil/$', views.actualizar_perfil, name='actualizar_perfil'),
    #url(r'^usuario/modificar_cuenta/$', views.actualizar_cuenta, name='actualizar_cuenta'),
    #url(r'^usuario/configuracion/$', views.configuraciones_usuario, name='configuraciones_usuario'),
    url(r'^usuario/password/cambiar/$', password_change, {'template_name': 'registration/password_change_form.html'}, 
        name='password_change'),
    url(r'^usuario/password/cambiar/hecho/$', password_change_done, {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),
    #url(r'^umedia/', include('user_media.urls')),
    #url(r'^usuario/actualizar_foto/$', views.upload_pic, name='subir_foto'),
    url(r'^mensaje/agregar_carta/$', views.upload_carta, name='subir_carta'),
    url(r'^mensaje/agregar_audio/$', views.upload_audio, name='subir_audio'),
    url(r'^mensaje/agregar_video/$', views.upload_video, name='subir_video'),
    #url(r'^perfil/(?P<username>\w+)/fotos/$', views.ver_imagenes_usuario, name='ver_imagenes_usuario'),
    url(r'^usuario/activar/(?P<codigo>\w+)/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', administrar.views.activarcuenta, name='activacion'),
]