# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-29 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_dine_query_current_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='dine_query',
            name='current_city',
            field=models.CharField(default='Chicago', max_length=20),
            preserve_default=False,
        ),
    ]
