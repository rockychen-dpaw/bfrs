# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-28 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfrs', '0014_auto_20170428_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='bushfire',
            name='assistance_req',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, b'Yes'), (2, b'No'), (3, b'Unknown')], null=True),
        ),
        migrations.AddField(
            model_name='bushfire',
            name='dispatch_pw',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, b'Yes'), (2, b'No'), (3, b'Monitoring only')], null=True),
        ),
        migrations.AddField(
            model_name='bushfire',
            name='other_tenure',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, b'Private'), (2, b'Crown')], null=True),
        ),
    ]
