from django.conf.urls import url, include
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete, password_change, password_change_done

import administrar.views
from usuario import views
from usuario.views import listar_cartas, listar_audio, listar_video


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^usuario/modificar_perfil/$', views.actualizar_perfil, name='actualizar_perfil'),
    url(r'^usuario/modificar_cuenta/$', views.actualizar_cuenta, name='actualizar_cuenta'),
    url(r'^usuario/configuracion/$', views.configuraciones_usuario, name='configuraciones_usuario'),
    url(r'^usuario/password/cambiar/$', password_change, {'template_name': 'registration/password_change_form.html'}, 
        name='password_change'),
    url(r'^usuario/password/cambiar/hecho/$', password_change_done, {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),
    url(r'^usuario/password/reset/$', password_reset, {'template_name': 'registration/password_reset_form.html'}, 
        name='password_reset'),
    url(r'^usuario/password/reset/hecho/$', password_reset_done, {'template_name': 'registration/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^usuario/password/reset/confirmar/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^usuario/password/reset/completo/$', password_reset_complete, {'template_name': 'registration/password_reset_complete.html'},
        name='password_reset_complete'),
    #url(r'^umedia/', include('user_media.urls')),
    #url(r'^usuario/actualizar_foto/$', views.upload_pic, name='subir_foto'),
    url(r'^mensaje/agregar_carta/$', views.upload_carta, name='subir_carta'),
    url(r'^mensaje/lista_cartas/$', listar_cartas.as_view(), name='lista_cartas'),
    url(r'^mensaje/detalle_carta/(?P<pk>[0-9]+)/$', views.carta_detalle, name='detalles_carta'),

    url(r'^mensaje/agregar_audio/$', views.upload_audio, name='subir_audio'),
    url(r'^mensaje/lista_audio/$', listar_audio.as_view(), name='lista_audio'),
    url(r'^mensaje/detalle_audio/(?P<pk>[0-9]+)/$', views.audio_detalle, name='detalles_audio'),

    url(r'^mensaje/agregar_video/$', views.upload_video, name='subir_video'),
    url(r'^mensaje/lista_video/$', listar_video.as_view(), name='lista_video'),
    url(r'^mensaje/detalle_video/(?P<pk>[0-9]+)/$', views.video_detalle, name='detalles_video'),

    url(r'^usuario/configuracion/$', views.configuraciones_usuario, name='configuraciones_usuario'),

    #url(r'^perfil/(?P<username>\w+)/fotos/$', views.ver_imagenes_usuario, name='ver_imagenes_usuario'),
    url(r'^usuario/activar/(?P<codigo>\w+)/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', administrar.views.activarcuenta, name='activacion'),
]