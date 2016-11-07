from django.contrib import admin
from paquetes.models import Membresia

# Register your models here.

class MembresiaAdmin(admin.ModelAdmin):
	model = Membresia


admin.site.register(Membresia, MembresiaAdmin)