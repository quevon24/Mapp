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
    file_ids = forms.CharField(required=False,widget=forms.HiddenInput(attrs={'class' : 'id_file_ids'}))
    contenido = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Perfil_carta
        fields = ('contenido', 'file_ids', 'contacto')
        widgets = {
        'user': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(Usuario_cartas, self).__init__(*args, **kwargs)
        self.fields['contacto'].queryset = Contactos.objects.filter(
                                        user_id=self.instance.user)

    def save(self, commit=True):
        media = super(Usuario_cartas, self).save(commit=False)
        if commit:
            media.save()
            print self.instance.pk
            inst = self.instance
            file_ids = [x for x in self.cleaned_data.get('file_ids').split(',') if x]
            print file_ids
            for file_id in file_ids:
                print file_id  
                f = Perfil_carta_archivo.objects.get(id=file_id)
                f.update(carta=inst)
                #a = FilesUpload(section=inst,attachment=f)
                #a.save()
        return media



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

class form_agregar_contacto(forms.ModelForm):
    class Meta:
        model = Contactos
        fields = ('nombre', 'email1', 'tel1', 'tel2', 'direccion')
