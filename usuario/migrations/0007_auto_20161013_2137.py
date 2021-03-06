# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-13 21:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import usuario.models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_auto_20161011_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil_carta_archivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=500)),
                ('archivo', models.FileField(blank=True, null=True, upload_to=usuario.models.user_directoryfile_path, validators=[usuario.models.validar_carta])),
            ],
        ),
        migrations.RemoveField(
            model_name='perfil_carta',
            name='archivo',
        ),
        migrations.AddField(
            model_name='perfil_carta_archivo',
            name='carta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Perfil_carta'),
        ),
    ]
