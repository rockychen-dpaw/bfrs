# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-22 06:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bfrs', '0014_auto_20170517_1200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agency',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='areaburnt',
            options={},
        ),
        migrations.AlterModelOptions(
            name='bushfire',
            options={},
        ),
        migrations.AlterModelOptions(
            name='cause',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='damage',
            options={},
        ),
        migrations.AlterModelOptions(
            name='damagetype',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='firebehaviour',
            options={},
        ),
        migrations.AlterModelOptions(
            name='fueltype',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='injury',
            options={},
        ),
        migrations.AlterModelOptions(
            name='injurytype',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='snapshothistory',
            options={},
        ),
        migrations.AlterModelOptions(
            name='tenure',
            options={'ordering': ['id']},
        ),
    ]