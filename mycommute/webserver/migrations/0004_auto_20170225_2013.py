# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0003_auto_20170225_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='cost',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='trip',
            name='stop',
            field=models.IntegerField(default=-1),
        ),
    ]
