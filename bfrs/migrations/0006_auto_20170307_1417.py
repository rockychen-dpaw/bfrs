# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-07 06:17
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfrs', '0005_auto_20170307_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bushfire',
            name='area',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name=b'Final Fire Area (ha)'),
        ),
    ]