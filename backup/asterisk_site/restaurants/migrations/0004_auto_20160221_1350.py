# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-21 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_dine_query_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dine_query',
            name='day',
            field=models.CharField(max_length=10),
        ),
    ]
