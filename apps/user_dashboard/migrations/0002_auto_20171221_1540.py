# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-21 23:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_level',
            field=models.IntegerField(max_length=255),
        ),
    ]