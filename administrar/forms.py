# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from models import *
from django import forms


class Registrar(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(Registrar, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].widget.attrs\
            .update({
                'placeholder': 'Usuario',
                'class': 'form-control'
            })
        self.fields['first_name'].widget.attrs\
            .update({
                'placeholder': 'Nombre(s)',
                'class': 'form-control'
            })
        self.fields['last_name'].widget.attrs\
            .update({
                'placeholder': 'Apellido(s)',
                'class': 'form-control'
            })
        self.fields['email'].widget.attrs\
            .update({
                'placeholder': 'Correo Electronico',
                'class': 'form-control'
            })
        self.fields['password'].widget.attrs\
            .update({
                'placeholder': 'Contraseña',
                'class': 'form-control'
            })