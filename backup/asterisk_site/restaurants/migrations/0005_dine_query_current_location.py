# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-29 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_auto_20160221_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='dine_query',
            name='current_location',
            field=models.CharField(default='5228 South Woodlawn Ave.', max_length=100),
            preserve_default=False,
        ),
    ]
