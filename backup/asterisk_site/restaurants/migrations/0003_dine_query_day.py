# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-21 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_auto_20160221_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='dine_query',
            name='day',
            field=models.CharField(default=2, max_length=64),
            preserve_default=False,
        ),
    ]