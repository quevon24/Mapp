# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from models import *
from django import forms


class Registrar(forms.ModelForm):

	error_messages = {
		'duplicate_username': 'Nombre de usuario ya existente',
		'duplicate_email': 'Email ya existente',
		'min_length': 'Contraseña minimo 8 caracteres',
		'password_sec_digit': 'Contraseña debe contener al menos un digito',
		'password_sec_char': 'Contraseña debe contener al menos una letra'
	}
	
	class Meta:
		model = User
		fields = ('username','first_name', 'last_name', 'email', 'password')

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User._default_manager.get(username=username)
			# si usuario existe, error en form
			raise forms.ValidationError( 
			  self.error_messages['duplicate_username'],  # mensaje personalizado
			  code='duplicate_username',   # poner mensaje
				)
		except User.DoesNotExist:
			return username # si no existe, entonces esta disponible

	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			User._default_manager.get(email=email)
			# si usuario existe, error en form
			raise forms.ValidationError( 
			  self.error_messages['duplicate_email'],  # mensaje personalizado
			  code='duplicate_email',   # poner mensaje
				)
		except User.DoesNotExist:
			return email # si no existe, entonces esta disponible

	def clean_password(self):
		MIN_LENGTH = 8
		password = self.cleaned_data["password"]
		# si no hay longitud minima de password, muestra error en form
		if len(password) < MIN_LENGTH:
			raise forms.ValidationError(self.error_messages['min_length'], code='min_length',)
		# si no hay un digito minimo, error en form
		if not any(char.isdigit() for char in password):
			raise forms.ValidationError(self.error_messages['password_sec_digit'], code='password_sec_digit',)
		# si no hay una letra minimo, error en form
		if not any(char.isalpha() for char in password):
			raise forms.ValidationError(self.error_messages['password_sec_char'], code='password_sec_char',)

		return password


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