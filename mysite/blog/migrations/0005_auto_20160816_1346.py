# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-16 04:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160816_1341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trends',
            old_name='totla_requests',
            new_name='total_requests',
        ),
    ]
