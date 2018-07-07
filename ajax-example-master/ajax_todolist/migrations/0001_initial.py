# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('ip_addr', models.GenericIPAddressField()),
            ],
        ),
    ]
