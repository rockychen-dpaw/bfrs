# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-08-08 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfrs', '0011_auto_20180521_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='bushfire',
            name='fire_bombing_req',
            field=models.NullBooleanField(verbose_name=b'Fire Bombing Required'),
        ),
        migrations.AddField(
            model_name='bushfiresnapshot',
            name='fire_bombing_req',
            field=models.NullBooleanField(verbose_name=b'Fire Bombing Required'),
        ),
        migrations.AlterField(
            model_name='bushfire',
            name='report_status',
            field=models.PositiveSmallIntegerField(choices=[(1, b'Initial Fire Report'), (2, b'Notifications Submitted'), (3, b'Report Authorised'), (4, b'Reviewed'), (5, b'Invalidated'), (6, b'Outstanding Fires'), (100, b'Merged'), (101, b'Duplicated')], default=1, editable=False),
        ),
        migrations.AlterField(
            model_name='bushfire',
            name='reporting_year',
            field=models.PositiveSmallIntegerField(blank=True, default=2018, verbose_name=b'Reporting Year'),
        ),
        migrations.AlterField(
            model_name='bushfire',
            name='year',
            field=models.PositiveSmallIntegerField(default=2018, verbose_name=b'Financial Year'),
        ),
        migrations.AlterField(
            model_name='bushfiresnapshot',
            name='report_status',
            field=models.PositiveSmallIntegerField(choices=[(1, b'Initial Fire Report'), (2, b'Notifications Submitted'), (3, b'Report Authorised'), (4, b'Reviewed'), (5, b'Invalidated'), (6, b'Outstanding Fires'), (100, b'Merged'), (101, b'Duplicated')], default=1, editable=False),
        ),
        migrations.AlterField(
            model_name='bushfiresnapshot',
            name='reporting_year',
            field=models.PositiveSmallIntegerField(blank=True, default=2018, verbose_name=b'Reporting Year'),
        ),
        migrations.AlterField(
            model_name='bushfiresnapshot',
            name='year',
            field=models.PositiveSmallIntegerField(default=2018, verbose_name=b'Financial Year'),
        ),
    ]
