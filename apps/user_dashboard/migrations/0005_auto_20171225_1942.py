# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-26 03:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0004_user_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='user_dashboard.User'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='written_messages', to='user_dashboard.User'),
        ),
    ]
