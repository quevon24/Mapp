from django.contrib import admin
from usuario.models import Perfil_carta, Perfil_audio, Perfil_video
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from usuario.models import Perfil

class CartaAdmin(admin.ModelAdmin):
	model = Perfil_carta
	list_display = ('fecha',)

class VozAdmin(admin.ModelAdmin):
	model = Perfil_audio
	list_display = ('fecha',)

class VideoAdmin(admin.ModelAdmin):
	model = Perfil_video
	list_display = ('fecha',)

class PerfilAdmin(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilAdmin, )

admin.site.register(Perfil_carta, CartaAdmin)
admin.site.register(Perfil_audio, VozAdmin)
admin.site.register(Perfil_video, VideoAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)