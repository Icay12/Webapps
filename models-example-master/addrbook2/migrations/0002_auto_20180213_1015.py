# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-13 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addrbook2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='entry',
            name='city',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='entry',
            name='country',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
