# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-24 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0003_auto_20171222_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='desc',
            field=models.TextField(default='hi'),
            preserve_default=False,
        ),
    ]
