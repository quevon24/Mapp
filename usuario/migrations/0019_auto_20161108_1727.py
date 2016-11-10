# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 17:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import usuario.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuario', '0018_auto_20161107_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil_video_archivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=500, null=True)),
                ('archivo', models.FileField(blank=True, null=True, upload_to=usuario.models.user_directoryfile_path)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='perfil_video',
            name='archivo',
        ),
        migrations.RemoveField(
            model_name='perfil_video',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='perfil_video',
            name='email',
        ),
        migrations.RemoveField(
            model_name='perfil_video',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='perfil_video',
            name='tel1',
        ),
        migrations.RemoveField(
            model_name='perfil_video',
            name='tel2',
        ),
        migrations.AddField(
            model_name='perfil_video',
            name='contacto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.Contactos'),
        ),
        migrations.AddField(
            model_name='perfil_video',
            name='descripcion',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='perfil_video_archivo',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.Perfil_video'),
        ),
    ]