# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-13 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0019_auto_20161108_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactos',
            name='tel2',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]