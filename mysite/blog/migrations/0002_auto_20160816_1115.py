# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-16 02:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_transfer_size', models.DecimalField(decimal_places=2, max_digits=5)),
                ('totla_requests', models.DecimalField(decimal_places=2, max_digits=5)),
                ('html_transfer_size', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 16, 2, 15, 23, 677623, tzinfo=utc)),
        ),
    ]
