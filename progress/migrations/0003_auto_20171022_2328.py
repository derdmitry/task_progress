# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-22 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0002_target_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='target',
            field=models.SmallIntegerField(default=0),
        ),
    ]