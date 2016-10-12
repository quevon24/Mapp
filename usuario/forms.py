# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from models import *
from django import forms
from ckeditor.widgets import CKEditorWidget



class Usuarioform(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class Perfilform(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('edad', 'telefono', 'celular', 'sexo',
        'direccion', 'descripcion')

class Usuario_cartas(forms.ModelForm):
    contenido = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Perfil_carta
        fields = ('contenido', 'archivo', 'email', 'tel1', 'tel2')
        widgets = {
        'user': forms.HiddenInput(),
        }

class Usuario_audios(forms.ModelForm):
    class Meta:
        model = Perfil_audio
        fields = ('archivo', 'email', 'tel1', 'tel2')
        widgets = {
        'user': forms.HiddenInput(),
        }

class Usuario_videos(forms.ModelForm):
    class Meta:
        model = Perfil_video
        fields = ('archivo','nombre', 'email', 'tel1', 'tel2', 'direccion', 'formato')
        widgets = {
        'user': forms.HiddenInput(),
        }