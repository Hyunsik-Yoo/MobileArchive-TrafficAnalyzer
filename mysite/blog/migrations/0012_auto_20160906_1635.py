# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-06 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20160906_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trends',
            name='date',
            field=models.DecimalField(decimal_places=0, default=1473114921000, max_digits=15),
        ),
    ]