# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from models import *
from django import forms


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
    class Meta:
        model = Perfil_carta
        fields = ('imagen','descripcion')
        widgets = {
        'user': forms.HiddenInput(),
        }