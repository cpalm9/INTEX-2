# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 02:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20170405_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='uniqueproduct',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
