from django.conf.urls import url, include
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete, password_change, password_change_done
from django.views.generic import CreateView, DeleteView, ListView

import administrar.views
from usuario import views
from usuario.views import listar_cartas, listar_audio, listar_video, PictureCreateView, PictureDeleteView1, listar_contactos, PictureCreateView_audio, PictureCreateView_video


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^chaining/', include('smart_selects.urls')),
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

    # Cartas
    url(r'^mensaje/agregar-carta/$', views.crear_carta, name='crear_carta'),
    url(r'^mensaje/lista-cartas/$', listar_cartas.as_view(), name='lista_cartas'),
    url(r'^mensaje/detalle-carta/(?P<pk>[0-9]+)/$', views.carta_detalle, name='detalles_carta'),
    url(r'^mensaje/editar-carta/(?P<pk>[0-9]+)/$', views.editar_carta, name='editar_carta'),
    url(r'^mensaje/subir-carta/$', PictureCreateView.as_view(), name='upload_carta'),
    url(r'^borrar-archivo-carta/(?P<pk>\d+)/$', views.borrar_archivo_carta, name='borrar_archivo_carta'),
    url(r'^obtener-archivos-cartas/(?P<cartaid>[0-9]+)/$', views.obtener_archivos_cartas, name='obtener_archivos_cartas'),
    url(r'^mensaje/pago-editar-carta/$', views.pagar_edicion_carta, name='pagar_edicion_carta'),

    # Audio
    url(r'^mensaje/agregar-audio/$', views.crear_audio, name='crear_audio'),
    url(r'^mensaje/lista-audio/$', listar_audio.as_view(), name='lista_audio'),
    url(r'^mensaje/detalle-audio/(?P<pk>[0-9]+)/$', views.audio_detalle, name='detalles_audio'),
    url(r'^mensaje/editar-audio/(?P<pk>[0-9]+)/$', views.editar_audio, name='editar_audio'),
    url(r'^mensaje/subir-audio/$', PictureCreateView_audio.as_view(), name='upload_audio'),
    url(r'^borrar-archivo-audio/(?P<pk>\d+)/$', views.borrar_archivo_audio, name='borrar_archivo_audio'),
    url(r'^obtener-archivos-audio/(?P<audioid>[0-9]+)/$', views.obtener_archivos_audio, name='obtener_archivos_audio'),

    # Video
    url(r'^mensaje/agregar-video/$', views.crear_video, name='crear_video'),
    url(r'^mensaje/lista-video/$', listar_video.as_view(), name='lista_video'),
    url(r'^mensaje/detalle-video/(?P<pk>[0-9]+)/$', views.video_detalle, name='detalles_video'),
    url(r'^mensaje/editar-video/(?P<pk>[0-9]+)/$', views.editar_video, name='editar_video'),
    url(r'^mensaje/subir-video/$', PictureCreateView_video.as_view(), name='upload_video'),
    url(r'^borrar-archivo-video/(?P<pk>\d+)/$', views.borrar_archivo_video, name='borrar_archivo_video'),
    url(r'^obtener-archivos-video/(?P<videoid>[0-9]+)/$', views.obtener_archivos_video, name='obtener_archivos_video'),

    # Usuario
    url(r'^usuario/configuracion/$', views.configuraciones_usuario, name='configuraciones_usuario'),

    # Activacion
    #url(r'^perfil/(?P<username>\w+)/fotos/$', views.ver_imagenes_usuario, name='ver_imagenes_usuario'),
    url(r'^usuario/activar/(?P<codigo>\w+)/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', administrar.views.activarcuenta, name='activacion'),

    # Contacto
    url(r'^contactos/agregar-contacto/$', views.agregar_contacto, name='agregar-contacto'),
    url(r'^obtener-datos-contacto/(?P<contactoid>[0-9]+)/$', views.ajax_datos_contacto, name='obtener-datos-contacto'),
    url(r'^obtener-contactos-usuario/(?P<pk>[0-9]+)/$', views.obtener_contactos_ajax, name='obtener-contactos-usuario'),
    url(r'^contactos/lista-contactos/$', listar_contactos.as_view(), name='lista_contactos'),
    url(r'^contactos/detalle-contacto/(?P<pk>[0-9]+)/$', views.contacto_detalle, name='detalles_contacto'),
    url(r'^contactos/editar-contacto/(?P<pk>[0-9]+)/$', views.editar_contacto, name='editar_contacto'),
    url(r'^contactos/agregar_ajax/$', views.agregar_contacto_ajax, name='agregar_contacto_ajax'),
       ]